"""
Management command to create/update indicator products in the store.
Run: python manage.py seed_indicators
"""
from django.core.management.base import BaseCommand
from landing.models import IndicatorProduct


INDICATORS = [
    # Flagship: Professional All-in-One Platform - Rs.10,000
    {
        "name": "Gautam Singh Professional Suite - All-in-One Trading Platform",
        "slug": "gautam-singh-model-all-in-one",
        "short_description": "7 integrated modules: SMC Analysis, AI Pivot Forecast, EMA Crossover, Range Filter, Confluence Sniper, Dynamic VWAP & Volume Profile",
        "description": (
            "<strong>Gautam Singh Professional Suite v2.2.0</strong> - The ultimate all-in-one TradingView indicator system "
            "engineered for professional traders. Integrates 7 powerful trading modules into a single, toggle-controlled platform "
            "with unified Gautam Singh Master Dashboard, consensus market status, and integrated backtesting analytics.<br><br>"
            "<strong>Complete Module Suite:</strong><br>"
            "1. Smart Money Concepts (SMC) + Order Block Analysis + Fair Value Gap Detection<br>"
            "2. AI-Powered Next Pivot Forecast Module<br>"
            "3. Triple EMA Crossover (9/26/50) with Auto SL/TP<br>"
            "4. Range Filter + Zero-Lag Moving Average (ZLMA) Levels<br>"
            "5. Confluence Sniper (10-point Precision Scoring)<br>"
            "6. Dynamic Swing VWAP with ATR Adaptive Bands<br>"
            "7. Volume Profile + Fixed Range POC Analysis<br><br>"
            "<strong>Premium Features:</strong><br>"
            "Gautam Singh Master Control Dashboard | 5-Module Market Consensus | Integrated Backtesting | "
            "Multi-Market Support | All Timeframes | Bar-Close Confirmation | Lifetime Updates<br><br>"
            "<strong>One-time investment - lifetime access to professional-grade trading tools.</strong>"
        ),
        "price": 10000,
        "pine_script_file": "gowthamsingh/indacter/merged_indicator.pine",
        "features": (
            "7 Professional Trading Modules\n"
            "Integrated Gautam Singh Master Dashboard\n"
            "5-Module Consensus Market Status\n"
            "Smart Money Concepts Analysis\n"
            "AI Next Pivot Forecasting\n"
            "Triple EMA Crossover System\n"
            "Dynamic Swing VWAP Analysis\n"
            "Volume Profile Integration\n"
            "Confluence Sniper Engine\n"
            "Automated Risk Management\n"
            "Integrated Backtesting Suite\n"
            "Multi-Market Support | All Timeframes\n"
            "Priority Professional Support"
        ),
        "is_active": True,
        "is_popular": True,
        "sort_order": 1,
        "subscription_days": 0,  # 0 = lifetime, no expiry
    },

    # Monthly subscription: Rs.999/mo
    {
        "name": "Gautam Singh Professional Suite - Monthly Access",
        "slug": "gautam-singh-model-triple-nine",
        "short_description": "Full monthly access to Gautam Singh Professional Suite with all 7 modules. Flexible subscription - cancel anytime.",
        "description": (
            "<strong>Gautam Singh Professional Suite - Monthly Subscription (Rs.999/month)</strong><br><br>"
            "Experience professional trading with complete access to all 7 integrated modules of the Gautam Singh suite. "
            "All features unlock with flexible month-to-month billing - cancel whenever you choose.<br><br>"
            "<strong>Full Access to:</strong><br>"
            "All 7 Trading Modules | Gautam Singh Master Dashboard | Market Consensus System | "
            "Backtesting Tools | Real-time Analytics<br><br>"
            "Renews automatically every 30 days. No long-term commitment required.<br><br>"
            "<em>Professional trading tools at an accessible monthly rate.</em>"
        ),
        "price": 999,
        "pine_script_file": "gowthamsingh/indacter/merged_indicator.pine",
        "features": (
            "All 7 Trading Modules Included\n"
            "Gautam Singh Master Dashboard\n"
            "Monthly Flexible Subscription\n"
            "Cancel Anytime\n"
            "Market Consensus System\n"
            "Backtesting Suite\n"
            "Real-time Analytics\n"
            "Professional Support\n"
            "Auto-Renewal Every 30 Days"
        ),
        "is_active": True,
        "is_popular": False,
        "sort_order": 4,
        "subscription_days": 30,
    },

    # Quarterly plan: Rs.4,999 / 3 months
    {
        "name": "Gautam Singh Professional Suite - Quarterly Plan",
        "slug": "gautam-singh-model-quarterly",
        "short_description": "3-month access to complete Gautam Singh Professional Suite. Best value for committed traders.",
        "description": (
            "<strong>Gautam Singh Professional Suite - 90-Day Quarterly Plan (Rs.4,999)</strong><br><br>"
            "Unlock 90 days of complete access to all 7 professional trading modules. "
            "Get all features of the Gautam Singh suite at the best value for active traders.<br><br>"
            "<strong>Full Access to:</strong><br>"
            "All 7 Integrated Trading Modules | Complete Analytics | Backtesting Suite | "
            "Master Dashboard | Market Consensus System<br><br>"
            "Expires after 90 days. Re-subscribe to continue seamlessly.<br><br>"
            "<em>Best value for serious traders - save 25% vs monthly pricing.</em>"
        ),
        "price": 4999,
        "pine_script_file": "gowthamsingh/indacter/merged_indicator.pine",
        "features": (
            "All 7 Trading Modules\n"
            "90-Day Access (3 Months)\n"
            "Best Value Plan\n"
            "Gautam Singh Master Dashboard\n"
            "Complete Market Consensus\n"
            "Backtesting Suite\n"
            "Real-time Analytics\n"
            "Professional Grade Tools\n"
            "Seamless Re-subscription"
        ),
        "is_active": True,
        "is_popular": True,
        "sort_order": 2,
        "subscription_days": 90,
    },

    # Legacy v1 - Renamed
    {
        "name": "Gautam Singh AI Intelligence - Core Edition",
        "slug": "gowtham-singh-ai-model",
        "short_description": "AI-powered intelligent signals with automatic risk management, precise TP/SL levels, and multi-timeframe trend analysis.",
        "description": (
            "<strong>Gautam Singh AI Intelligence - Core Edition</strong><br><br>"
            "The foundational AI-powered trading indicator engineered by Gautam Singh. Features intelligent buy/sell signal generation "
            "with automatic Take Profit and Stop Loss calculation, plus advanced multi-timeframe trend detection.<br><br>"
            "<strong>Key Features:</strong><br>"
            "AI-Powered Signal Generation | Automatic TP & SL Management | Multi-Timeframe Trend Analysis | "
            "Fair Value Gap Detection | Liquidity Zone Identification | No Repaint Confirmation<br><br>"
            "Professional support included with lifetime updates."
        ),
        "price": 2000,
        "pine_script_file": "Gowtham_Singh_AI_Model.pine",
        "features": (
            "AI-Powered Intelligent Signals\n"
            "Automatic TP & SL Management\n"
            "Multi-Timeframe Trend Detection\n"
            "Fair Value Gap Analysis\n"
            "Liquidity Zone Mapping\n"
            "No Repaint Confirmation\n"
            "Works on All Markets\n"
            "All Timeframes Supported\n"
            "Professional Support\n"
            "Lifetime Updates"
        ),
        "is_active": True,
        "is_popular": False,
        "sort_order": 3,
    },

    # Legacy v2 - Renamed
    {
        "name": "Gautam Singh AI Intelligence - Advanced Edition",
        "slug": "gowtham-singh-ai-model-v2",
        "short_description": "Enhanced AI system with Smart Money Concepts, order flow analysis, and precision signal filtering for professional traders.",
        "description": (
            "<strong>Gautam Singh AI Intelligence - Advanced Edition</strong><br><br>"
            "Next-generation intelligent system from Gautam Singh. Combines Smart Money Concepts methodology with advanced order flow analysis "
            "and multi-layer signal filtering for maximum trading precision.<br><br>"
            "<strong>Advanced Features:</strong><br>"
            "Smart Money Concepts Integration | Order Flow Analysis | Enhanced Signal Filtering | "
            "Liquidity Level Detection | Market Structure Analysis | Professional Dashboard<br><br>"
            "Designed for advanced traders seeking institutional-grade analysis tools."
        ),
        "price": 2500,
        "pine_script_file": "Gowtham_Singh_AI_Model_v2.pine",
        "features": (
            "Core AI Features\n"
            "Smart Money Concepts (SMC)\n"
            "Order Flow Analysis\n"
            "Enhanced Signal Filtering\n"
            "Advanced Liquidity Detection\n"
            "Professional Dashboard\n"
            "Market Structure Analysis\n"
            "Signal Confidence Scoring\n"
            "Professional Support\n"
            "Lifetime Updates"
        ),
        "is_active": True,
        "is_popular": False,
        "sort_order": 4,
    },

    # EMA System - Professional Name
    {
        "name": "Gautam Singh EMA Momentum - Professional Crossover System",
        "slug": "ema-gautam-singh",
        "short_description": "Triple EMA (9/26/50) confluence system with swing-based risk management and 1:2 reward-to-risk automation.",
        "description": (
            "<strong>Gautam Singh EMA Momentum - Professional Crossover System</strong><br><br>"
            "A sophisticated triple EMA system designed by Gautam Singh for precision swing trading. "
            "Automatically identifies convergence/divergence patterns (9/26/50) with intelligent swing-based stop-loss placement "
            "and professional 1:2 risk-to-reward take-profit targets.<br><br>"
            "<strong>Professional Features:</strong><br>"
            "Triple EMA Confluence Detection (9/26/50) | Swing-Based Stop Loss | "
            "1:2 Risk-Reward Automation | Real-time SL/TP Lines | Customizable Alert System<br><br>"
            "<strong>Ideal for:</strong> Swing traders | EMA-based strategies | Forex, Crypto & Stock markets | All timeframes<br><br>"
            "<strong>One-time investment - lifetime access to professional EMA system.</strong>"
        ),
        "price": 999,
        "pine_script_file": "gowthamsingh/indacter/EMA_GAUTAM_SINGH.pine",
        "features": (
            "Triple EMA Confluence (9/26/50)\n"
            "Professional Signal Generation\n"
            "Swing-Based Stop Loss\n"
            "1:2 Risk-Reward Automation\n"
            "Real-time SL & TP Display\n"
            "Customizable Alert System\n"
            "Multi-Market Support\n"
            "All Timeframes\n"
            "No Repaint Confirmation\n"
            "Professional Support\n"
            "Lifetime Updates"
        ),
        "is_active": True,
        "is_popular": True,
        "sort_order": 5,
        "subscription_days": 0,
    },

    # Dynamic VWAP - Professional Name
    {
        "name": "Gautam Singh Volume Dynamics - Adaptive VWAP System",
        "slug": "dynamic-swing-vwap",
        "short_description": "Intelligent volume-weighted price analysis with swing adaptability, multi-timeframe support, and professional signal generation.",
        "description": (
            "<strong>Gautam Singh Volume Dynamics - Adaptive VWAP Professional System</strong><br><br>"
            "An institutional-grade volume-weighted price analysis system created by Gautam Singh. "
            "Features adaptive swing point detection that dynamically adjusts to market conditions, delivering premium trading signals "
            "backed by professional volume analysis across all market conditions and timeframes.<br><br>"
            "<strong>Professional Capabilities:</strong><br>"
            "Adaptive VWAP Calculation | Swing-Point Auto-Detection | Dynamic Band Adjustment | "
            "Multi-Timeframe Compatibility | Real-time Market Insights | High-Probability Signal Generation<br><br>"
            "<strong>Ideal for:</strong> Volume-based traders | Position traders | Swing analysts | Institutional traders<br><br>"
            "<strong>One-time investment - lifetime access to professional volume analysis.</strong>"
        ),
        "price": 4999,
        "pine_script_file": "gowthamsingh/indacter/Dynamic_Swing_VWAP.pine",
        "features": (
            "Adaptive VWAP Calculation\n"
            "Dynamic Swing Detection\n"
            "Multi-Timeframe Compatible\n"
            "Professional Signal Generation\n"
            "Volume-Weighted Analysis\n"
            "Swing Point Automation\n"
            "Customizable Bands\n"
            "Real-time Market Insights\n"
            "High-Probability Setups\n"
            "Professional Risk Management\n"
            "No Repaint Confirmation\n"
            "Lifetime Professional Support"
        ),
        "is_active": True,
        "is_popular": True,
        "sort_order": 6,
        "subscription_days": 0,
    },

    # Confluence Sniper - Professional Name
    {
        "name": "Gautam Singh Confluence Sniper - 10-Point Precision System",
        "slug": "precision-sniper",
        "short_description": "10-point confluence scoring engine with multi-timeframe analysis, adaptive trailing stops, and 3-level take-profit management.",
        "description": (
            "<strong>Gautam Singh Confluence Sniper - 10-Point Precision Scoring System</strong><br><br>"
            "A sophisticated precision scoring system engineered by Gautam Singh for institutional-grade trade execution. "
            "Combines advanced 10-point confluence analysis with multi-timeframe filtering, intelligent trailing stop management, "
            "and 3-level take-profit optimization for maximum trade probability and risk-adjusted returns.<br><br>"
            "<strong>Professional System Components:</strong><br>"
            "10-Point Confluence Scoring | Multi-Timeframe Trend Filter | "
            "3-Level TP Management (TP1/TP2/TP3) | Adaptive Trailing Stop | Structure-Based Stop Loss | "
            "Real-time Professional Dashboard | 4 Strategic Presets | Webhook & Alert Integration<br><br>"
            "<strong>Ideal for:</strong> Professional traders | Confluence-based strategies | Risk management optimization<br><br>"
            "<strong>One-time investment - lifetime access to precision trading system.</strong>"
        ),
        "price": 2999,
        "pine_script_file": "gowthamsingh/indacter/Precision_Sniper.pine",
        "features": (
            "10-Point Confluence Scoring\n"
            "Multi-Timeframe Trend Filter\n"
            "3-Level Take-Profit Management\n"
            "Adaptive Trailing Stop\n"
            "Structure-Based Stop Loss\n"
            "Professional Dashboard\n"
            "4 Strategic Presets\n"
            "Webhook Integration\n"
            "Advanced Alert System\n"
            "Professional Risk Management\n"
            "High-Conviction Signals\n"
            "Lifetime Professional Support"
        ),
        "is_active": True,
        "is_popular": True,
        "sort_order": 7,
        "subscription_days": 0,
    },
]


class Command(BaseCommand):
    help = "Seed / update all indicator products in the Gautam Singh Store"

    def handle(self, *args, **options):
        created_count = 0
        updated_count = 0

        self.stdout.write("\n=== Gautam Singh Store - Seeding Products ===\n")

        for data in INDICATORS:
            obj, created = IndicatorProduct.objects.update_or_create(
                slug=data["slug"],
                defaults=data,
            )
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(
                    f"  [CREATED] {obj.name} -- Rs.{obj.price}"
                ))
            else:
                updated_count += 1
                self.stdout.write(self.style.WARNING(
                    f"  [UPDATED] {obj.name} -- Rs.{obj.price}"
                ))

        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS(
            f"Done! Created {created_count}, updated {updated_count} product(s)."
        ))
        self.stdout.write(self.style.NOTICE(
            "Manage products in Django admin: /admin/landing/indicatorproduct/"
        ))
