from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("portfolio/", views.portfolio_view, name="portfolio"),
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),

    # Store & Indicators
    path("store/", views.store_view, name="store"),
    path("indicator/<slug:slug>/", views.indicator_detail, name="indicator_detail"),
    path("indicator/", views.indicator_view, name="indicator"),
    path("my-purchases/", views.my_purchases, name="my_purchases"),

    # Razorpay Payment
    path("api/create-order/<slug:slug>/", views.create_razorpay_order, name="create_order"),
    path("api/verify-payment/", views.verify_payment, name="verify_payment"),
    path("api/create-course-order/<slug:slug>/", views.create_course_order, name="create_course_order"),
    path("api/verify-course-payment/", views.verify_course_payment, name="verify_course_payment"),
    path("webhook/razorpay/", views.razorpay_webhook, name="razorpay_webhook"),

    # Existing pages
    path("market-analysis/", views.market_analysis_view, name="market_analysis"),
    path("vip-trades/", views.vip_trades_view, name="vip_trades"),
    path("redeem-vip/", views.redeem_vip_code, name="redeem_vip_code"),

    # Support Center
    path("support/", views.support_view, name="support"),
    
    # Contact Page
    path("contact/", views.contact_view, name="contact"),
    path("contact/submit/", views.contact_submit, name="contact_submit"),
]
