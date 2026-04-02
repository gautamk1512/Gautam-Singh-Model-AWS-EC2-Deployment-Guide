from django.contrib import admin
from .models import IndicatorProduct, Purchase, MarketAnalysis, VIPTrade, VIPAccessCode


@admin.register(IndicatorProduct)
class IndicatorProductAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "is_active", "is_popular", "sort_order", "created_at")
    list_filter = ("is_active", "is_popular")
    list_editable = ("price", "is_active", "is_popular", "sort_order")
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    fieldsets = (
        (None, {
            "fields": ("name", "slug", "short_description", "description", "price"),
        }),
        ("Product Settings", {
            "fields": ("pine_script_file", "features", "is_active", "is_popular", "sort_order"),
        }),
    )


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ("user", "product", "amount", "status", "razorpay_payment_id", "purchased_at")
    list_filter = ("status", "product")
    search_fields = ("user__username", "user__email", "razorpay_order_id", "razorpay_payment_id")
    readonly_fields = ("razorpay_order_id", "razorpay_payment_id", "razorpay_signature", "purchased_at")

    actions = ["mark_as_paid"]

    @admin.action(description="Mark selected purchases as Paid (manual override)")
    def mark_as_paid(self, request, queryset):
        count = queryset.update(status="paid")
        self.message_user(request, f"Marked {count} purchase(s) as paid.")


@admin.register(MarketAnalysis)
class MarketAnalysisAdmin(admin.ModelAdmin):
    list_display = ("pair", "timeframe", "title", "published_at")
    list_filter = ("pair", "timeframe")
    search_fields = ("title", "pair")


@admin.register(VIPTrade)
class VIPTradeAdmin(admin.ModelAdmin):
    list_display = ("pair", "direction", "entry_price", "stop_loss", "take_profit", "status", "pnl_pips", "published_at")
    list_filter = ("status", "direction")
    search_fields = ("pair",)


@admin.register(VIPAccessCode)
class VIPAccessCodeAdmin(admin.ModelAdmin):
    list_display = ("code", "user", "is_used", "is_active", "activated_at", "expires_at", "created_at")
    list_filter = ("is_used", "is_active")
    search_fields = ("code", "user__username")
    readonly_fields = ("code", "activated_at", "expires_at")
    actions = ["generate_codes"]

    @admin.action(description="Generate 10 new VIP codes")
    def generate_codes(self, request, queryset):
        codes = []
        for _ in range(10):
            c = VIPAccessCode.objects.create()
            codes.append(c.code)
        self.message_user(request, f"Generated 10 codes: {', '.join(codes)}")
