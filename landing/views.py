import razorpay
import json
import os
import uuid
from datetime import timedelta

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
    VIPTrade, VIPAccessCode, Course, CoursePurchase,
)

# Razorpay client
razorpay_client = razorpay.Client(
    auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
)


def home(request):
    products = IndicatorProduct.objects.filter(is_active=True)
    return render(request, "landing/index.html", {"products": products})


def custom_404(request, exception=None):
    """Custom 404 handler — shows a styled page for any invalid route."""
    return render(request, "landing/404.html", {
        "request_path": request.path,
    }, status=404)


def portfolio_view(request):
    """Display Gautam Singh's professional portfolio"""
    free_courses = Course.objects.filter(course_type="free", is_active=True).order_by("sort_order", "-created_at")
    premium_courses = Course.objects.filter(course_type="premium", is_active=True).order_by("sort_order", "-created_at")
    unlocked_course_ids = set()
    if request.user.is_authenticated:
        unlocked_course_ids = set(
            CoursePurchase.objects.filter(
                user=request.user,
                status="paid",
                valid_until__gte=timezone.now()
            ).values_list("course_id", flat=True)
        )

    portfolio_data = {
        "name": "Gautam Singh",
        "title": "Full Stack Developer & Trading Systems Engineer",
        "location": "Vadodara, India",
        "email": "gautamk1512@gmail.com",
        "bio": "Passionate Full Stack Developer with expertise in building dynamic, end-to-end web applications. I specialize in both front-end and back-end development, crafting seamless user experiences. I combine my programming skills with active trading experience to develop innovative trading solutions and indicators.",
        "years_experience": "5+",
        "name_carousel_photos": [
            "https://images.unsplash.com/photo-1521119989659-a83eee488004?auto=format&fit=crop&w=900&q=80",
            "https://images.unsplash.com/photo-1522556189639-b150d9f9e3ff?auto=format&fit=crop&w=900&q=80",
            "https://images.unsplash.com/photo-1506863530036-1efeddceb993?auto=format&fit=crop&w=900&q=80",
            "https://images.unsplash.com/photo-1507679799987-c73779587ccf?auto=format&fit=crop&w=900&q=80",
            "https://images.unsplash.com/photo-1519085360753-af0119f7cbe7?auto=format&fit=crop&w=900&q=80",
        ],
        "free_courses": free_courses,
        "premium_courses": premium_courses,
        "unlocked_course_ids": unlocked_course_ids,
        "razorpay_key_id": settings.RAZORPAY_KEY_ID,
        "skills": [
            {"name": "Backend", "tools": "Django, Python, Node.js, Java"},
            {"name": "Frontend", "tools": "HTML5, CSS3, JavaScript, AngularJS"},
            {"name": "Database", "tools": "MongoDB, Firebase, MySQL"},
            {"name": "DevOps", "tools": "Docker, AWS, Heroku, Linux"},
            {"name": "Trading", "tools": "Pine Script, TradingView, Technical Analysis"},
            {"name": "Tools", "tools": "Git, Figma, Arduino, Kafka"},
        ],
        "projects": [
            {
                "title": "Student Management System",
                "description": "Django-based LMS managing student records, courses, and enrollment with role-based access control.",
                "tech": "Django, Python, MySQL",
                "link": "https://github.com/gautamk1512/gautamk1512-studentmanagement_by_django-main"
            },
            {
                "title": "Gautam Singh AI Trading Model",
                "description": "Advanced Pine Script indicator providing AI-powered trading signals with automated TP/SL for forex, crypto, and stocks.",
                "tech": "Pine Script v5, TradingView",
                "link": "https://github.com/gautamk1512"
            },
            {
                "title": "AWS EC2 Deployment Guide",
                "description": "Complete deployment guide for the Gautam Singh Model on AWS infrastructure.",
                "tech": "AWS, EC2, DevOps",
                "link": "https://github.com/gautamk1512/Gautam-Singh-Model-AWS-EC2-Deployment-Guide"
            },
            {
                "title": "TradingView MCP Integration",
                "description": "Model Context Protocol integration for TradingView with advanced streaming capabilities.",
                "tech": "JavaScript, TradingView API",
                "link": "https://github.com/gautamk1512/tradingview-mcp"
            },
        ],
        "achievements": [
            "Developed AI-powered trading indicator used by 5000+ active traders",
            "Created full-stack LMS platform managing education workflows",
            "92 GitHub repositories showcasing diverse technical expertise",
            "276+ contributions in the past year demonstrating consistent development",
            "Successfully deployed trading systems on AWS infrastructure"
        ],
        "social": {
            "github": "https://github.com/gautamk1512",
            "linkedin": "https://www.linkedin.com/in/gautam-singh-696003193/",
            "instagram": "https://www.instagram.com/gautams1512/",
            "youtube": "https://www.youtube.com/@fachwitheinsteingautamsing928",
            "blog": "https://gautamk1512.blogspot.com/",
        }
    }
    return render(request, "landing/portfolio.html", portfolio_data)


@login_required
@require_POST
def create_course_order(request, slug):
    course = get_object_or_404(Course, slug=slug, is_active=True, course_type="premium")

    if CoursePurchase.objects.filter(
        user=request.user, course=course, status="paid", valid_until__gte=timezone.now()
    ).exists():
        return JsonResponse({"error": "You already have active access to this course."}, status=400)

    try:
        # Guard: check if keys are configured
        if "REPLACE_WITH" in settings.RAZORPAY_KEY_ID or not settings.RAZORPAY_KEY_ID.startswith(("rzp_test_", "rzp_live_")):
            return JsonResponse({
                "error": "Payment gateway is not configured. Please contact the site administrator."
            }, status=503)

        order_data = {
            "amount": course.price_in_paise(),
            "currency": "INR",
            "notes": {
                "user_id": str(request.user.id),
                "course_slug": course.slug,
                "course_title": course.title,
            },
        }
        razorpay_order = razorpay_client.order.create(data=order_data)
        purchase, created = CoursePurchase.objects.get_or_create(
            user=request.user,
            course=course,
            defaults={
                "amount": course.price,
                "status": "pending",
                "razorpay_order_id": razorpay_order["id"],
            },
        )
        if not created:
            purchase.amount = course.price
            purchase.status = "pending"
            purchase.razorpay_order_id = razorpay_order["id"]
            purchase.save()

        return JsonResponse({
            "order_id": razorpay_order["id"],
            "amount": razorpay_order["amount"],
            "currency": razorpay_order["currency"],
            "key_id": settings.RAZORPAY_KEY_ID,
            "course_title": course.title,
            "user_email": request.user.email,
            "user_name": request.user.get_full_name() or request.user.username,
        })
    except Exception as e:
        return JsonResponse({"error": f"Payment error: {str(e)}"}, status=500)


@login_required
@require_POST
def verify_course_payment(request):
    try:
        data = json.loads(request.body)
        razorpay_order_id = data.get("razorpay_order_id")
        razorpay_payment_id = data.get("razorpay_payment_id")
        razorpay_signature = data.get("razorpay_signature")
        course_slug = data.get("course_slug")

        if not all([razorpay_order_id, razorpay_payment_id, razorpay_signature, course_slug]):
            return JsonResponse({"error": "Missing payment details."}, status=400)

        params = {
            "razorpay_order_id": razorpay_order_id,
            "razorpay_payment_id": razorpay_payment_id,
            "razorpay_signature": razorpay_signature,
        }
        razorpay_client.utility.verify_payment_signature(params)

        purchase = CoursePurchase.objects.get(user=request.user, razorpay_order_id=razorpay_order_id)
        purchase.razorpay_payment_id = razorpay_payment_id
        purchase.razorpay_signature = razorpay_signature
        purchase.status = "paid"
        purchase.valid_until = timezone.now() + timedelta(days=30)
        purchase.save()

        return JsonResponse({
            "success": True,
            "message": "Payment successful! Premium course unlocked.",
        })
    except CoursePurchase.DoesNotExist:
        return JsonResponse({"error": "Course purchase record not found."}, status=404)
    except razorpay.errors.SignatureVerificationError:
        return JsonResponse({"error": "Payment verification failed."}, status=400)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid request data."}, status=400)
    except Exception as e:
        return JsonResponse({"error": f"Verification error: {str(e)}"}, status=500)


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

    def _activate_purchase(purchase):
        purchase.status = "paid"
        days = purchase.product.subscription_days if hasattr(purchase.product, 'subscription_days') else 30
        if purchase.is_subscription and days > 0:
            purchase.valid_until = timezone.now() + timedelta(days=days)
        purchase.access_password = uuid.uuid4().hex[:8]
        purchase.save()

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
        _activate_purchase(purchase)
        if not created:
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
    # Guard: check if keys are configured
    if "REPLACE_WITH" in settings.RAZORPAY_KEY_ID or not settings.RAZORPAY_KEY_ID.startswith(("rzp_test_", "rzp_live_")):
        return JsonResponse({
            "error": "Payment gateway is not configured. Please contact the site administrator to set up Razorpay API keys."
        }, status=503)

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
            if purchase.is_subscription:
                days = purchase.product.subscription_days if hasattr(purchase.product, 'subscription_days') else 30
                if days > 0:
                    purchase.valid_until = timezone.now() + timedelta(days=days)
            purchase.access_password = uuid.uuid4().hex[:8]
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
                    if purchase.is_subscription:
                        days = purchase.product.subscription_days if hasattr(purchase.product, 'subscription_days') else 30
                        if days > 0:
                            purchase.valid_until = timezone.now() + timedelta(days=days)
                    purchase.access_password = purchase.access_password or uuid.uuid4().hex[:8]
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
    """Show individual indicator instructions and ask for TradingView username."""
    product = get_object_or_404(IndicatorProduct, slug=slug, is_active=True)

    # Check if user has purchased this indicator
    purchase = Purchase.objects.filter(
        user=request.user, product=product, status="paid"
    ).first()
    has_access = purchase is not None
    is_expired = False

    if has_access and purchase.is_subscription and purchase.valid_until and purchase.valid_until < timezone.now():
        has_access = False
        is_expired = True

    indicator_code = ""

    if has_access:
        try:
            pine_path = os.path.join(settings.BASE_DIR, product.pine_script_file)
            with open(pine_path, "r", encoding="utf-8") as f:
                indicator_code = f.read()
                
            expiry_timestamp = "0"
            if purchase.is_subscription and purchase.valid_until:
                expiry_timestamp = str(int(purchase.valid_until.timestamp() * 1000))
                
            pwd = purchase.access_password if purchase.access_password else "N/A"
            
            indicator_code = indicator_code.replace("{{EXPIRY_TIMESTAMP}}", expiry_timestamp)
            indicator_code = indicator_code.replace("{{ACCESS_PASSWORD}}", pwd)
        except Exception:
            indicator_code = "// Indicator file not found or reading failed. Contact support."

    return render(request, "landing/indicator_detail.html", {
        "product": product,
        "has_access": has_access,
        "is_expired": is_expired,
        "purchase": purchase,
        "indicator_code": indicator_code,
        "razorpay_key_id": settings.RAZORPAY_KEY_ID,
        "demo_mode": getattr(settings, 'DEMO_MODE', False)
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


# ═══════════ SUPPORT CENTER ═══════════

def support_view(request):
    """Support Center page with AI chat, human support, payments FAQ, and rules."""
    return render(request, "landing/support.html")


# ═══════════ CONTACT PAGE ═══════════

def contact_view(request):
    """Contact & Support page with contact form and support information."""
    return render(request, "landing/contact_support.html")


def contact_submit(request):
    """Handle contact form submission and save to database."""
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        email = request.POST.get("email", "").strip()
        subject = request.POST.get("subject", "").strip()
        message = request.POST.get("message", "").strip()
        
        # Basic validation
        if not all([name, email, subject, message]):
            return JsonResponse({
                "success": False,
                "message": "Please fill in all required fields."
            })
        
        # Email validation
        if "@" not in email or "." not in email:
            return JsonResponse({
                "success": False,
                "message": "Please enter a valid email address."
            })
        
        # Message length validation
        if len(message) < 10:
            return JsonResponse({
                "success": False,
                "message": "Message must be at least 10 characters long."
            })
        
        # Save to database
        try:
            from .models import ContactMessage
            contact_message = ContactMessage.objects.create(
                name=name,
                email=email,
                subject=subject,
                message=message
            )
            
            # Log the contact form submission
            import logging
            logger = logging.getLogger(__name__)
            logger.info(f"Contact form submitted - ID: {contact_message.id}, Name: {name}, Email: {email}, Subject: {subject}")
            
            return JsonResponse({
                "success": True,
                "message": "Thank you for your message! We'll get back to you soon."
            })
            
        except Exception as e:
            logger = logging.getLogger(__name__)
            logger.error(f"Error saving contact form: {str(e)}")
            return JsonResponse({
                "success": False,
                "message": "An error occurred while saving your message. Please try again."
            })
    
    return JsonResponse({
        "success": False,
        "message": "Invalid request method."
    })
