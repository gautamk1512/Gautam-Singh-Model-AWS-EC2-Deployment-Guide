<p align="center">
  <img src="https://img.shields.io/badge/Django-6.0-092E20?style=for-the-badge&logo=django&logoColor=white" />
  <img src="https://img.shields.io/badge/Python-3.12+-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/AWS-EC2-FF9900?style=for-the-badge&logo=amazonaws&logoColor=white" />
  <img src="https://img.shields.io/badge/Nginx-009639?style=for-the-badge&logo=nginx&logoColor=white" />
  <img src="https://img.shields.io/badge/Gunicorn-499848?style=for-the-badge&logo=gunicorn&logoColor=white" />
  <img src="https://img.shields.io/badge/Razorpay-02042B?style=for-the-badge&logo=razorpay&logoColor=white" />
</p>

# 🚀 Gautam Singh Model — Trading Indicator Platform

> A full-stack Django web application for selling & distributing premium TradingView Pine Script indicators, with Razorpay payment integration, Google OAuth login, VIP trade signals, and market analysis feeds.

---

## ✨ Features

### 🛒 Indicator Store
- Browse and purchase premium TradingView indicators
- Per-indicator pricing with Razorpay payment gateway
- Secure Pine Script code delivery after purchase
- Demo mode for testing without real payments

### 📊 Bundled Pine Script Indicators
| Indicator | Description |
|-----------|-------------|
| **SMC + Next Pivot** | Smart Money Concepts with market structure, order blocks, FVG, and AI-powered pivot forecasting |
| **EMA Crossover (9/26/50)** | Triple EMA crossover strategy with automatic SL/TP at 1:2 risk-reward |
| **Range Filter + Zero-Lag MA** | Range-based trend filter combined with zero-lag moving average trend levels |
| **Precision Sniper** | Multi-confluence scoring engine (10-point system) with EMA ribbon, MACD, RSI, ADX, VWAP, and HTF bias |
| **All-in-One Merged** | All indicators combined with a switchboard to toggle each module on/off |

### 🔐 Authentication & Access Control
- Django allauth with Google OAuth 2.0 login
- Username + email registration
- Purchase-gated indicator access

### 📈 VIP Trades
- Live trade signals (Buy/Sell) with Entry, SL, and TP
- VIP access codes with 30-day expiry
- Trade status tracking (Active, TP Hit, SL Hit)

### 📰 Market Analysis
- Admin-published analysis with charts
- Key levels and timeframe breakdown

### 🔒 License System (Pine Script)
- Time-based 10-day license for indicators
- Admin-configurable activation dates
- License key + user validation
- Auto-expiry with renewal flow

---

## 🏗️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **Backend** | Django 6.0, Python 3.12+ |
| **Frontend** | HTML5, CSS3, JavaScript |
| **Database** | SQLite (dev) — can swap to PostgreSQL |
| **Auth** | django-allauth, Google OAuth 2.0 |
| **Payments** | Razorpay API |
| **Server** | Gunicorn + Nginx |
| **Static Files** | WhiteNoise |
| **Hosting** | AWS EC2 (Ubuntu) |

---

## 📁 Project Structure

```
Gautamsinghmodle/
├── manage.py
├── requirements.txt
├── .gitignore
├── .env.example
│
├── gowthamsingh/                # Django project config
│   ├── settings.py              # Production-ready (env vars)
│   ├── urls.py
│   ├── wsgi.py
│   └── indacter/                # Pine Script indicators
│       ├── merged_indicator.pine
│       ├── EMA_GAUTAM_SINGH.pine
│       ├── gautam_singh_range_nolag.pine
│       ├── Precision_Sniper_Gautam_Singh.pine
│       └── Precision_Sniper.pine
│
├── landing/                     # Main Django app
│   ├── models.py                # IndicatorProduct, Purchase, VIPTrade, etc.
│   ├── views.py                 # All views + Razorpay integration
│   ├── urls.py
│   ├── admin.py
│   ├── forms.py
│   ├── templates/landing/       # HTML templates
│   └── static/landing/          # CSS, JS, images
│
└── deploy/                      # Deployment configs
    ├── setup_server.sh          # One-click EC2 setup script
    ├── gunicorn.service         # Systemd service
    ├── nginx_gautamsingh        # Nginx site config
    └── .env.example             # Environment variables template
```

---

## 🚀 Quick Start (Local Development)

### 1. Clone the repo
```bash
git clone https://github.com/gautamk1512/Gautam-Singh-Model-AWS-EC2-Deployment-Guide.git
cd Gautam-Singh-Model-AWS-EC2-Deployment-Guide
```

### 2. Create virtual environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run migrations
```bash
python manage.py migrate
```

### 5. Create admin user
```bash
python manage.py createsuperuser
```

### 6. Run the server
```bash
python manage.py runserver
```

Visit **http://127.0.0.1:8000** 🎉

---

## ☁️ AWS EC2 Deployment

### Prerequisites
- AWS account with EC2 access
- Ubuntu 24.04 LTS instance (t2.micro for free tier)
- SSH key pair (`.pem` file)

### One-Command Deploy
```bash
# SSH into your EC2 instance
ssh -i your-key.pem ubuntu@YOUR_EC2_IP

# Clone the repo
git clone https://github.com/gautamk1512/Gautam-Singh-Model-AWS-EC2-Deployment-Guide.git Gautamsinghmodle

# Run the automated deployment
chmod +x Gautamsinghmodle/deploy/setup_server.sh
bash Gautamsinghmodle/deploy/setup_server.sh
```

### What the script does:
1. ✅ Updates Ubuntu & installs Python3, Nginx, pip
2. ✅ Configures UFW firewall (SSH + HTTP + HTTPS)
3. ✅ Creates Python virtual environment & installs packages
4. ✅ Generates `.env` with random secret key
5. ✅ Runs `collectstatic` and `migrate`
6. ✅ Sets up Gunicorn as a systemd service
7. ✅ Configures Nginx as reverse proxy
8. ✅ Starts everything automatically

### Post-Deployment
```bash
# Edit environment variables
nano /home/ubuntu/Gautamsinghmodle/.env

# Update Nginx server_name with your IP
sudo nano /etc/nginx/sites-available/gautamsingh

# Restart services
sudo systemctl restart gunicorn nginx

# Create admin account
cd /home/ubuntu/Gautamsinghmodle && source venv/bin/activate
python3 manage.py createsuperuser
```

### Add SSL (Optional)
```bash
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com
```

---

## ⚙️ Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DJANGO_ENV` | `production` or `development` | `development` |
| `DJANGO_SECRET_KEY` | Random secret key | Insecure default |
| `DJANGO_ALLOWED_HOSTS` | Comma-separated hosts | `localhost,127.0.0.1` |
| `DEMO_MODE` | Bypass Razorpay payments | `True` |
| `RAZORPAY_KEY_ID` | Razorpay API key | — |
| `RAZORPAY_KEY_SECRET` | Razorpay API secret | — |
| `GOOGLE_CLIENT_ID` | Google OAuth client ID | — |
| `GOOGLE_CLIENT_SECRET` | Google OAuth secret | — |
| `SECURE_SSL_REDIRECT` | Force HTTPS | `False` |

---

## 🛠️ Useful Commands

```bash
# Check service status
sudo systemctl status gunicorn
sudo systemctl status nginx

# View logs
sudo journalctl -u gunicorn -f
sudo tail -f /var/log/nginx/error.log

# After code updates
cd /home/ubuntu/Gautamsinghmodle
source venv/bin/activate
git pull origin main
python3 manage.py collectstatic --noinput
python3 manage.py migrate
sudo systemctl restart gunicorn
```

---

## 👨‍💻 Author

**Gautam Singh**
- Trading Indicator Developer
- Full-Stack Web Developer
- TradingView: [@gautamsingh1207200](https://www.tradingview.com/u/gautamsingh1207200/)

---

## 📄 License

This project is proprietary software. All Pine Script indicators are protected by a license system. Unauthorized distribution is prohibited.

---

<p align="center">
  Made with ❤️ by <strong>Gautam Singh</strong>
</p>
