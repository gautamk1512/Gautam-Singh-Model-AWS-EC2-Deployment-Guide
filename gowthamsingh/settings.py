"""
Django settings for gowthamsingh project.
Production-ready with environment variable support.
"""

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# ─── ENVIRONMENT ───
# Set DJANGO_ENV=production on your server
ENVIRONMENT = os.environ.get("DJANGO_ENV", "development")
IS_PRODUCTION = ENVIRONMENT == "production"

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get(
    "DJANGO_SECRET_KEY",
    "django-insecure-7-n^r-=$6c=b5)upwao61kiuebac1=(4agmp5e21p_!ic14u&7",
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = not IS_PRODUCTION

# ─── Hosts ───
ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")
if IS_PRODUCTION:
    CSRF_TRUSTED_ORIGINS = [
        f"https://{host}" for host in ALLOWED_HOSTS if host
    ]

# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "landing",
    # allauth
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",
]

SITE_ID = 1

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # Serve static files in production
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "allauth.account.middleware.AccountMiddleware",
]

ROOT_URLCONF = "gowthamsingh.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "gowthamsingh.wsgi.application"


# Database
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Kolkata"
USE_I18N = True
USE_TZ = True


# ─── Static files ───
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ─── Auth ───
LOGIN_URL = "/login/"
LOGIN_REDIRECT_URL = "/indicator/"
LOGOUT_REDIRECT_URL = "/"

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]

# ─── Allauth ───
ACCOUNT_LOGIN_ON_SIGNUP = True
ACCOUNT_LOGIN_METHODS = {"email", "username"}          # replaces deprecated ACCOUNT_AUTHENTICATION_METHOD
ACCOUNT_SIGNUP_FIELDS = ["email*", "username*", "password1*", "password2*"]  # replaces deprecated ACCOUNT_EMAIL_REQUIRED
ACCOUNT_EMAIL_VERIFICATION = "none"
SOCIALACCOUNT_LOGIN_ON_GET = True
SOCIALACCOUNT_AUTO_SIGNUP = True

SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "SCOPE": ["profile", "email"],
        "AUTH_PARAMS": {"access_type": "online"},
        "APP": {
            "client_id": os.environ.get("GOOGLE_CLIENT_ID", ""),
            "secret": os.environ.get("GOOGLE_CLIENT_SECRET", ""),
            "key": "",
        },
    }
}

# ─── Demo Mode ───
# Set DEMO_MODE=True  → Payment is bypassed (for testing, no real money)
# Set DEMO_MODE=False → Real Razorpay LIVE payment is used
DEMO_MODE = os.environ.get("DEMO_MODE", "False").lower() == "true"  # LIVE MODE — real payments active

# ─── Razorpay Keys ───
# HOW TO GET KEYS:
#   1. Go to https://dashboard.razorpay.com
#   2. Login → Settings → API Keys → Generate Key
#   3. Copy Key ID and Key Secret
#   4. For TEST mode keys start with: rzp_test_XXXX
#   5. For LIVE mode keys start with: rzp_live_XXXX
#
# Set these via environment variables OR replace the fallback strings below:
RAZORPAY_KEY_ID = os.environ.get("RAZORPAY_KEY_ID", "rzp_live_B2EmEyw89Cfll5")
RAZORPAY_KEY_SECRET = os.environ.get("RAZORPAY_KEY_SECRET", "4KzIo4bQRnkYFPmwPz36de0x")
RAZORPAY_WEBHOOK_SECRET = os.environ.get("RAZORPAY_WEBHOOK_SECRET", "REPLACE_WITH_YOUR_WEBHOOK_SECRET")

# ─── Razorpay Key Validation ───
_rzp_key = RAZORPAY_KEY_ID
if not DEMO_MODE and ("REPLACE_WITH" in _rzp_key or not _rzp_key.startswith(("rzp_test_", "rzp_live_"))):
    import warnings
    warnings.warn(
        "\n\n🚨 PAYMENT GATEWAY ERROR: Razorpay keys are not configured!\n"
        "   RAZORPAY_KEY_ID is still a placeholder.\n"
        "   Go to https://dashboard.razorpay.com → Settings → API Keys\n"
        "   Then set RAZORPAY_KEY_ID and RAZORPAY_KEY_SECRET in your environment.\n"
        "   OR set DEMO_MODE=True to test without real payments.\n",
        stacklevel=2,
    )

# ─── Production Security ───
if IS_PRODUCTION:
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    X_FRAME_OPTIONS = "DENY"
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_SSL_REDIRECT = os.environ.get("SECURE_SSL_REDIRECT", "True").lower() == "true"
