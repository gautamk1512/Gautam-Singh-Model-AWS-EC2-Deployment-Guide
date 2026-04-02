"""
Management command to create initial indicator products.
Run: python manage.py seed_indicators
"""
from django.core.management.base import BaseCommand
from landing.models import IndicatorProduct


INDICATORS = [
    {
        "name": "Gowtham Singh AI Model",
        "slug": "gowtham-singh-ai-model",
        "short_description": "AI-powered trading indicator with buy/sell signals, TP/SL lines, and multi-timeframe trend analysis.",
        "description": "The flagship AI-powered TradingView indicator. Uses advanced machine learning to generate high-probability buy/sell signals with automatic Take Profit and Stop Loss levels.",
        "price": 2000,
        "pine_script_file": "Gowtham_Singh_AI_Model.pine",
        "features": "AI-powered Buy & Sell Signals\nAutomatic TP & SL Lines\nMulti-timeframe Trend Dashboard\nFair Value Gap Detection\nLiquidity Zone Mapping\nNo Repaint Guarantee\nWorks on all markets & timeframes\nFull Support & Updates",
        "is_active": True,
        "is_popular": True,
        "sort_order": 1,
    },
    {
        "name": "Gowtham Singh AI Model V2",
        "slug": "gowtham-singh-ai-model-v2",
        "short_description": "Enhanced V2 edition with advanced smart money concepts and improved signal accuracy.",
        "description": "The next-generation of our AI indicator. Includes all V1 features plus enhanced Smart Money Concepts, order flow analysis, and improved signal filtering.",
        "price": 2500,
        "pine_script_file": "Gowtham_Singh_AI_Model_v2.pine",
        "features": "All V1 Features Included\nSmart Money Concepts (SMC)\nOrder Flow Analysis\nEnhanced Signal Filtering\nAdvanced Liquidity Detection\nImproved Dashboard\nPriority Support\nLifetime Updates",
        "is_active": True,
        "is_popular": False,
        "sort_order": 2,
    },
]


class Command(BaseCommand):
    help = "Seed initial indicator products into the database"

    def handle(self, *args, **options):
        created_count = 0
        updated_count = 0

        for data in INDICATORS:
            obj, created = IndicatorProduct.objects.update_or_create(
                slug=data["slug"],
                defaults=data,
            )
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f"  ✓ Created: {obj.name} — ₹{obj.price}"))
            else:
                updated_count += 1
                self.stdout.write(self.style.WARNING(f"  ↻ Updated: {obj.name} — ₹{obj.price}"))

        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS(
            f"Done! Created {created_count}, updated {updated_count} indicator(s)."
        ))
        self.stdout.write(self.style.NOTICE(
            "You can edit indicators in the Django admin: /admin/landing/indicatorproduct/"
        ))
