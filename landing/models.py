import secrets
import string

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.text import slugify
from datetime import timedelta


# ═══════════ INDICATOR PRODUCTS ═══════════

class IndicatorProduct(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    short_description = models.CharField(max_length=300, help_text="One-line description for the store card")
    description = models.TextField(help_text="Full description (supports HTML)")
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Price in INR (e.g. 1000.00)")
    pine_script_file = models.CharField(max_length=300, help_text="Filename of .pine file relative to BASE_DIR (e.g. Gautam_Singh_AI_Model.pine)")
    features = models.TextField(blank=True, help_text="One feature per line — displayed as bullet points on the store card")
    is_active = models.BooleanField(default=True, help_text="Visible in the store?")
    is_popular = models.BooleanField(default=False, help_text="Show 'Popular' badge")
    sort_order = models.IntegerField(default=0, help_text="Lower numbers appear first")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["sort_order", "created_at"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def price_in_paise(self):
        """Return price in paise for Razorpay API."""
        return int(self.price * 100)

    def get_features_list(self):
        """Return features as a list of strings."""
        if not self.features:
            return []
        return [f.strip() for f in self.features.strip().split("\n") if f.strip()]

    def __str__(self):
        return f"{self.name} — ₹{self.price}"


# ═══════════ PURCHASES ═══════════

PURCHASE_STATUS_CHOICES = [
    ("pending", "Pending"),
    ("paid", "Paid ✅"),
    ("failed", "Failed ❌"),
    ("refunded", "Refunded"),
]


class Purchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="purchases")
    product = models.ForeignKey(IndicatorProduct, on_delete=models.CASCADE, related_name="purchases")
    razorpay_order_id = models.CharField(max_length=255, blank=True, null=True)
    razorpay_payment_id = models.CharField(max_length=255, blank=True, null=True)
    razorpay_signature = models.CharField(max_length=500, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, help_text="Amount paid in INR")
    status = models.CharField(max_length=20, choices=PURCHASE_STATUS_CHOICES, default="pending")
    purchased_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-purchased_at"]
        unique_together = [("user", "product")]

    def __str__(self):
        return f"{self.user.username} — {self.product.name} [{self.get_status_display()}]"


# ═══════════ MARKET ANALYSIS ═══════════

class MarketAnalysis(models.Model):
    title = models.CharField(max_length=200)
    pair = models.CharField(max_length=30, help_text="e.g. GBP/JPY, BTC/USDT")
    timeframe = models.CharField(max_length=20, help_text="e.g. 15-Min, 1H, 4H, Daily")
    image = models.ImageField(upload_to="analysis/", blank=True, null=True)
    key_levels = models.TextField(help_text="Key levels & analysis text")
    published_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-published_at"]
        verbose_name_plural = "Market Analyses"

    def __str__(self):
        return f"{self.pair} – {self.timeframe} ({self.published_at:%d %b %Y %H:%M})"


# ═══════════ VIP TRADES ═══════════

TRADE_DIRECTION_CHOICES = [
    ("buy", "Buy"),
    ("sell", "Sell"),
]

TRADE_STATUS_CHOICES = [
    ("active", "Active"),
    ("tp_hit", "TP Hit ✅"),
    ("sl_hit", "SL Hit ❌"),
    ("closed", "Closed"),
]

class VIPTrade(models.Model):
    pair = models.CharField(max_length=30, help_text="e.g. EUR/USD, XAUUSD")
    direction = models.CharField(max_length=4, choices=TRADE_DIRECTION_CHOICES)
    entry_price = models.DecimalField(max_digits=12, decimal_places=5)
    stop_loss = models.DecimalField(max_digits=12, decimal_places=5)
    take_profit = models.DecimalField(max_digits=12, decimal_places=5)
    status = models.CharField(max_length=10, choices=TRADE_STATUS_CHOICES, default="active")
    pnl_pips = models.DecimalField(max_digits=8, decimal_places=1, blank=True, null=True, help_text="Profit/loss in pips")
    notes = models.TextField(blank=True)
    published_at = models.DateTimeField(auto_now_add=True)
    closed_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ["-published_at"]

    def __str__(self):
        return f"{self.get_direction_display()} {self.pair} @ {self.entry_price} [{self.get_status_display()}]"


# ═══════════ VIP ACCESS CODES ═══════════

def generate_vip_code():
    """Generate a random 12-character alphanumeric code."""
    chars = string.ascii_uppercase + string.digits
    return ''.join(secrets.choice(chars) for _ in range(12))


class VIPAccessCode(models.Model):
    code = models.CharField(max_length=20, unique=True, default=generate_vip_code)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="vip_codes")
    is_used = models.BooleanField(default=False)
    activated_at = models.DateTimeField(null=True, blank=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def activate(self, user):
        """Redeem this code for a user — sets 30-day expiry."""
        self.user = user
        self.is_used = True
        self.activated_at = timezone.now()
        self.expires_at = timezone.now() + timedelta(days=30)
        self.is_active = True
        self.save()

    def is_valid(self):
        """Check if code is active and not expired."""
        if not self.is_active or not self.is_used:
            return False
        if self.expires_at and self.expires_at < timezone.now():
            return False
        return True

    def days_remaining(self):
        if not self.expires_at:
            return 0
        delta = self.expires_at - timezone.now()
        return max(0, delta.days)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        status = "Valid" if self.is_valid() else "Expired/Unused"
        user_str = self.user.username if self.user else "Unassigned"
        return f"{self.code} — {user_str} ({status})"
