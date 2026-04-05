import os
import requests
from django.core.management.base import BaseCommand
from django.conf import settings
from django.utils.dateparse import parse_datetime
from landing.models import YouTubeVideo, YouTubePlaylist

YOUTUBE_API_URL = "https://www.googleapis.com/youtube/v3"

class Command(BaseCommand):
    help = "Syncs playlists, videos, and live streams from the specified YouTube channel."

    def add_arguments(self, parser):
        parser.add_argument(
            '--handle',
            type=str,
            default='@fachwitheinsteingautamsing928',
            help='The YouTube channel handle (e.g. @channel). Default is @fachwitheinsteingautamsing928.'
        )

    def handle(self, *args, **options):
        api_key = getattr(settings, 'YOUTUBE_API_KEY', os.environ.get('YOUTUBE_API_KEY'))
        if not api_key:
            self.stdout.write(self.style.ERROR("YOUTUBE_API_KEY is not set in settings or environment."))
            return

        handle = options['handle']
        # YouTube requires handles to not start with '@' in the forHandle parameter in some cases,
        # but the docs say it should be @handle. We will pass it as is, but if it fails, fallback.
        handle_clean = handle if handle.startswith('@') else f"@{handle}"

        self.stdout.write(f"Fetching channel info for {handle_clean}...")
        
        # 1. Get Channel ID and Uploads Playlist ID
        channel_resp = requests.get(
            f"{YOUTUBE_API_URL}/channels",
            params={
                "part": "id,contentDetails",
                "forHandle": handle_clean,
                "key": api_key
            }
        ).json()

        if "items" not in channel_resp or not channel_resp["items"]:
            self.stdout.write(self.style.ERROR(f"Could not find channel for handle {handle_clean}."))
            self.stdout.write(str(channel_resp))
            return

        channel_id = channel_resp["items"][0]["id"]
        uploads_playlist_id = channel_resp["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]

        self.stdout.write(self.style.SUCCESS(f"Found Channel ID: {channel_id} | Uploads: {uploads_playlist_id}"))

        # 2. Sync Playlists
        self.stdout.write("Syncing Playlists...")
        playlists_resp = requests.get(
            f"{YOUTUBE_API_URL}/playlists",
            params={
                "part": "snippet",
                "channelId": channel_id,
                "maxResults": 50,
                "key": api_key
            }
        ).json()

        playlist_items = playlists_resp.get("items", [])
        for pl in playlist_items:
            pl_id = pl["id"]
            snippet = pl["snippet"]
            
            # Find best thumbnail
            thumbs = snippet.get("thumbnails", {})
            thumb_url = ""
            for res in ["maxres", "high", "medium", "default"]:
                if res in thumbs:
                    thumb_url = thumbs[res]["url"]
                    break

            YouTubePlaylist.objects.update_or_create(
                playlist_id=pl_id,
                defaults={
                    "title": snippet.get("title", ""),
                    "description": snippet.get("description", ""),
                    "thumbnail_url": thumb_url,
                    "published_at": parse_datetime(snippet["publishedAt"])
                }
            )
        self.stdout.write(self.style.SUCCESS(f"Synced {len(playlist_items)} playlists."))

        # 3. Sync Videos (From Uploads)
        self.stdout.write("Syncing Latest Uploads & Live Streams...")
        videos_resp = requests.get(
            f"{YOUTUBE_API_URL}/playlistItems",
            params={
                "part": "snippet,contentDetails",
                "playlistId": uploads_playlist_id,
                "maxResults": 50,
                "key": api_key
            }
        ).json()

        # Step 3.1: Gather Video IDs to bulk fetch video details (duration, live status, etc)
        video_items = videos_resp.get("items", [])
        video_ids = [v["contentDetails"]["videoId"] for v in video_items]

        if video_ids:
            # Bulk fetch details
            details_resp = requests.get(
                f"{YOUTUBE_API_URL}/videos",
                params={
                    "part": "snippet,contentDetails,statistics,liveStreamingDetails",
                    "id": ",".join(video_ids),
                    "key": api_key
                }
            ).json()

            for vid in details_resp.get("items", []):
                v_id = vid["id"]
                snippet = vid["snippet"]
                content_details = vid["contentDetails"]
                statistics = vid.get("statistics", {})
                live_details = vid.get("liveStreamingDetails", {})
                
                # Check if currently live
                is_live = False
                if snippet.get("liveBroadcastContent") == "live":
                    is_live = True

                # Find best thumbnail
                thumbs = snippet.get("thumbnails", {})
                thumb_url = ""
                for res in ["maxres", "high", "medium", "default"]:
                    if res in thumbs:
                        thumb_url = thumbs[res]["url"]
                        break
                
                YouTubeVideo.objects.update_or_create(
                    video_id=v_id,
                    defaults={
                        "title": snippet.get("title", ""),
                        "description": snippet.get("description", ""),
                        "thumbnail_url": thumb_url,
                        "published_at": parse_datetime(snippet["publishedAt"]),
                        "duration": content_details.get("duration", ""),
                        "view_count": int(statistics.get("viewCount", 0)),
                        "is_live": is_live,
                    }
                )

        self.stdout.write(self.style.SUCCESS(f"Synced {len(video_ids)} recent videos/streams."))

        # 4. Sync Playlist Videos
        # To organize series-wise, we fetch videos for each playlist and associate them.
        self.stdout.write("Associating videos with playlists series-wise...")
        for pl_obj in YouTubePlaylist.objects.all():
            pl_items_resp = requests.get(
                f"{YOUTUBE_API_URL}/playlistItems",
                params={
                    "part": "contentDetails",
                    "playlistId": pl_obj.playlist_id,
                    "maxResults": 50,
                    "key": api_key
                }
            ).json()

            pl_video_ids = [item["contentDetails"]["videoId"] for item in pl_items_resp.get("items", [])]
            # Update local videos that belong to this playlist
            if pl_video_ids:
                YouTubeVideo.objects.filter(video_id__in=pl_video_ids).update(playlist=pl_obj)

        self.stdout.write(self.style.SUCCESS("Successfully completed full YouTube Channel Sync!"))
