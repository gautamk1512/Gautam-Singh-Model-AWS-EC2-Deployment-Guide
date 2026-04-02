import razorpay
import json
import os

from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils import timezone

from .forms import RegisterForm
from .models import (
    IndicatorProduct, Purchase, MarketAnalysis,
    VIPTrade, VIPAccessCode,
)

# Razorpay client
razorpay_client = razorpay.Client(
    auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
)


def home(request):
    products = IndicatorProduct.objects.filter(is_active=True)
    return render(request, "landing/index.html", {"products": products})


# ═══════════ AUTH ═══════════

def register_view(request):
    if request.user.is_authenticated:
        return redirect("store")
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend="django.contrib.auth.backends.ModelBackend")
            messages.success(request, "Account created! Browse our indicators to get started.")
            return redirect("store")
    else:
        form = RegisterForm()
    return render(request, "landing/register.html", {"form": form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect("store")
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("store")
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, "landing/login.html")


def logout_view(request):
    logout(request)
    return redirect("home")


# ═══════════ INDICATOR STORE ═══════════

def store_view(request):
    """Public store page listing all indicators with prices."""
    products = IndicatorProduct.objects.filter(is_active=True)

    # For authenticated users, get their purchased product IDs
    purchased_ids = set()
    if request.user.is_authenticated:
        purchased_ids = set(
            Purchase.objects.filter(
                user=request.user, status="paid"
            ).values_list("product_id", flat=True)
        )

    return render(request, "landing/store.html", {
        "products": products,
        "purchased_ids": purchased_ids,
        "razorpay_key_id": settings.RAZORPAY_KEY_ID,
    })


# ═══════════ RAZORPAY CHECKOUT ═══════════

@login_required
@require_POST
def create_razorpay_order(request, slug):
    """Creates a Razorpay order for the given indicator product."""
    product = get_object_or_404(IndicatorProduct, slug=slug, is_active=True)

    # Check if already purchased
    if Purchase.objects.filter(user=request.user, product=product, status="paid").exists():
        return JsonResponse({"error": "You have already purchased this indicator."}, status=400)

    # ── DEMO MODE: bypass Razorpay, grant purchase directly ──
    if getattr(settings, "DEMO_MODE", False):
        purchase, created = Purchase.objects.get_or_create(
            user=request.user,
            product=product,
            defaults={
                "amount": product.price,
                "status": "paid",
                "razorpay_order_id": "demo_order",
                "razorpay_payment_id": "demo_payment",
            },
        )
        if not created:
            purchase.status = "paid"
            purchase.razorpay_order_id = "demo_order"
            purchase.razorpay_payment_id = "demo_payment"
            purchase.amount = product.price
            purchase.save()

        return JsonResponse({
            "demo": True,
            "message": f"[DEMO] {product.name} purchased! No payment charged.",
            "redirect_url": f"/indicator/{product.slug}/",
        })

    # ── LIVE MODE: create Razorpay order ──
    try:
        order_data = {
            "amount": product.price_in_paise(),
            "currency": "INR",
            "notes": {
                "user_id": str(request.user.id),
                "product_slug": product.slug,
                "product_name": product.name,
            },
        }
        razorpay_order = razorpay_client.order.create(data=order_data)

        # Create pending purchase record
        purchase, created = Purchase.objects.get_or_create(
            user=request.user,
            product=product,
            defaults={
                "amount": product.price,
                "status": "pending",
                "razorpay_order_id": razorpay_order["id"],
            },
        )
        if not created:
            purchase.razorpay_order_id = razorpay_order["id"]
            purchase.status = "pending"
            purchase.amount = product.price
            purchase.save()

        return JsonResponse({
            "order_id": razorpay_order["id"],
            "amount": razorpay_order["amount"],
            "currency": razorpay_order["currency"],
            "key_id": settings.RAZORPAY_KEY_ID,
            "product_name": product.name,
            "user_email": request.user.email,
            "user_name": request.user.get_full_name() or request.user.username,
        })

    except Exception as e:
        return JsonResponse({"error": f"Payment error: {str(e)}"}, status=500)


@login_required
@require_POST
def verify_payment(request):
    """Verify Razorpay payment after checkout and grant access."""
    try:
        data = json.loads(request.body)
        razorpay_order_id = data.get("razorpay_order_id")
        razorpay_payment_id = data.get("razorpay_payment_id")
        razorpay_signature = data.get("razorpay_signature")
        product_slug = data.get("product_slug")

        if not all([razorpay_order_id, razorpay_payment_id, razorpay_signature, product_slug]):
            return JsonResponse({"error": "Missing payment details."}, status=400)

        # Verify payment signature
        params = {
            "razorpay_order_id": razorpay_order_id,
            "razorpay_payment_id": razorpay_payment_id,
            "razorpay_signature": razorpay_signature,
        }
        razorpay_client.utility.verify_payment_signature(params)

        # Signature valid — update purchase record
        try:
            purchase = Purchase.objects.get(
                user=request.user,
                razorpay_order_id=razorpay_order_id,
            )
            purchase.razorpay_payment_id = razorpay_payment_id
            purchase.razorpay_signature = razorpay_signature
            purchase.status = "paid"
            purchase.save()

            return JsonResponse({
                "success": True,
                "message": f"Payment successful! You now have access to {purchase.product.name}.",
                "redirect_url": f"/indicator/{purchase.product.slug}/",
            })

        except Purchase.DoesNotExist:
            return JsonResponse({"error": "Purchase record not found."}, status=404)

    except razorpay.errors.SignatureVerificationError:
        return JsonResponse({"error": "Payment verification failed. Invalid signature."}, status=400)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid request data."}, status=400)
    except Exception as e:
        return JsonResponse({"error": f"Verification error: {str(e)}"}, status=500)


@csrf_exempt
@require_POST
def razorpay_webhook(request):
    """Webhook endpoint for Razorpay server-side payment confirmation."""
    try:
        webhook_secret = settings.RAZORPAY_WEBHOOK_SECRET
        webhook_signature = request.headers.get("X-Razorpay-Signature", "")
        webhook_body = request.body.decode("utf-8")

        # Verify webhook signature
        razorpay_client.utility.verify_webhook_signature(
            webhook_body, webhook_signature, webhook_secret
        )

        payload = json.loads(webhook_body)
        event = payload.get("event", "")

        if event == "payment.captured":
            payment = payload["payload"]["payment"]["entity"]
            order_id = payment.get("order_id")
            payment_id = payment.get("id")

            if order_id:
                try:
                    purchase = Purchase.objects.get(razorpay_order_id=order_id)
                    purchase.razorpay_payment_id = payment_id
                    purchase.status = "paid"
                    purchase.save()
                except Purchase.DoesNotExist:
                    pass  # Order not found — may be from another system

        elif event == "payment.failed":
            payment = payload["payload"]["payment"]["entity"]
            order_id = payment.get("order_id")

            if order_id:
                try:
                    purchase = Purchase.objects.get(razorpay_order_id=order_id)
                    if purchase.status != "paid":
                        purchase.status = "failed"
                        purchase.save()
                except Purchase.DoesNotExist:
                    pass

        return HttpResponse(status=200)

    except razorpay.errors.SignatureVerificationError:
        return HttpResponse("Invalid webhook signature", status=400)
    except Exception:
        return HttpResponse(status=500)


# ═══════════ INDICATOR ACCESS ═══════════

@login_required
def indicator_detail(request, slug):
    """Show individual indicator — code if purchased, locked preview if not."""
    product = get_object_or_404(IndicatorProduct, slug=slug, is_active=True)

    # Check if user has purchased this indicator
    has_access = Purchase.objects.filter(
        user=request.user, product=product, status="paid"
    ).exists()

    # Only read Pine Script code if user has access
    indicator_code = ""
    if has_access:
        try:
            pine_path = os.path.join(settings.BASE_DIR, product.pine_script_file)
            with open(pine_path, "r", encoding="utf-8") as f:
                indicator_code = f.read()
        except FileNotFoundError:
            indicator_code = "// Indicator file not found. Contact support."

    return render(request, "landing/indicator_detail.html", {
        "product": product,
        "has_access": has_access,
        "indicator_code": indicator_code,
        "razorpay_key_id": settings.RAZORPAY_KEY_ID,
    })


@login_required
def indicator_view(request):
    """Legacy indicator page — redirects to my purchases."""
    return redirect("my_purchases")


@login_required
def my_purchases(request):
    """Dashboard showing all purchased indicators."""
    purchases = Purchase.objects.filter(
        user=request.user, status="paid"
    ).select_related("product")

    return render(request, "landing/my_purchases.html", {
        "purchases": purchases,
    })


# ═══════════ MARKET ANALYSIS (FREE) ═══════════

def market_analysis_view(request):
    analyses = MarketAnalysis.objects.all()
    return render(request, "landing/market_analysis.html", {"analyses": analyses})


# ═══════════ VIP TRADES (GATED BY ACCESS CODE) ═══════════

def _get_user_vip_access(user):
    """Check if user has a valid VIP access code."""
    if not user.is_authenticated:
        return None
    vip_code = VIPAccessCode.objects.filter(user=user, is_used=True, is_active=True).first()
    if vip_code and vip_code.is_valid():
        return vip_code
    return None


def vip_trades_view(request):
    vip_code = _get_user_vip_access(request.user)
    has_vip_access = vip_code is not None

    active_trades = []
    closed_trades = []

    if has_vip_access:
        trades = VIPTrade.objects.all()
        active_trades = trades.filter(status="active")
        closed_trades = trades.exclude(status="active")

    return render(request, "landing/vip_trades.html", {
        "has_vip_access": has_vip_access,
        "vip_code": vip_code,
        "vip_days_left": vip_code.days_remaining() if vip_code else 0,
        "active_trades": active_trades,
        "closed_trades": closed_trades,
    })


@login_required
def redeem_vip_code(request):
    if request.method == "POST":
        code_input = request.POST.get("vip_code", "").strip().upper()

        if not code_input:
            messages.error(request, "Please enter a valid access code.")
            return redirect("vip_trades")

        try:
            vip_code = VIPAccessCode.objects.get(code=code_input)
        except VIPAccessCode.DoesNotExist:
            messages.error(request, "Invalid access code. Please check and try again.")
            return redirect("vip_trades")

        if vip_code.is_used:
            messages.error(request, "This code has already been used.")
            return redirect("vip_trades")

        if not vip_code.is_active:
            messages.error(request, "This code is no longer active.")
            return redirect("vip_trades")

        # Activate the code for the current user
        vip_code.activate(request.user)
        messages.success(request, f"✅ VIP Access activated! Your access is valid for 30 days (expires {vip_code.expires_at.strftime('%d %b %Y')}).")
        return redirect("vip_trades")

    return redirect("vip_trades")
