from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static

from landing.views import custom_404

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path("", include("landing.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Catch-all: any unmatched URL → custom 404 (works even with DEBUG=True)
urlpatterns += [
    re_path(r"^.*$", custom_404),
]

handler404 = "landing.views.custom_404"
