#!/bin/bash
# ═══════════════════════════════════════════════════════════
# Gautam Singh Model — EC2 Deployment Script
# Run this on your Ubuntu EC2 instance
# ═══════════════════════════════════════════════════════════
set -e

echo "═══════════════════════════════════════════════"
echo "  Gautam Singh Model — Server Setup"
echo "═══════════════════════════════════════════════"

# ─── Step 1: System Update ───
echo "[1/8] Updating system packages..."
sudo apt update && sudo apt upgrade -y

# ─── Step 2: Install Dependencies ───
echo "[2/8] Installing Python, Nginx, and tools..."
sudo apt install -y python3 python3-pip python3-venv nginx git ufw

# ─── Step 3: Firewall Setup ───
echo "[3/8] Configuring firewall..."
sudo ufw allow OpenSSH
sudo ufw allow 'Nginx Full'
sudo ufw --force enable

# ─── Step 4: Clone/Upload Project ───
echo "[4/8] Setting up project directory..."
cd /home/ubuntu
if [ ! -d "Gautamsinghmodle" ]; then
    echo "  → Project directory not found!"
    echo "  → Please upload your project first using SCP:"
    echo "     scp -i your-key.pem -r ./Gautamsinghmodle ubuntu@YOUR_IP:/home/ubuntu/"
    exit 1
fi

cd /home/ubuntu/Gautamsinghmodle

# ─── Step 5: Virtual Environment ───
echo "[5/8] Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# ─── Step 6: Django Setup ───
echo "[6/8] Configuring Django..."

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "  → Creating .env from template..."
    cp deploy/.env.example .env
    # Generate a random secret key
    SECRET=$(python3 -c "import secrets; print(secrets.token_urlsafe(50))")
    sed -i "s|CHANGE_ME_TO_A_RANDOM_50_CHAR_STRING|${SECRET}|" .env
    echo "  ⚠️  IMPORTANT: Edit .env and set your EC2 public IP!"
    echo "     nano /home/ubuntu/Gautamsinghmodle/.env"
fi

# Source env vars for Django commands
set -a; source .env; set +a

# Collect static files
python3 manage.py collectstatic --noinput

# Run migrations
python3 manage.py migrate

# ─── Step 7: Gunicorn Service ───
echo "[7/8] Setting up Gunicorn service..."
sudo cp deploy/gunicorn.service /etc/systemd/system/gunicorn.service
sudo systemctl daemon-reload
sudo systemctl enable gunicorn
sudo systemctl start gunicorn

# ─── Step 8: Nginx Configuration ───
echo "[8/8] Configuring Nginx..."
sudo cp deploy/nginx_gautamsingh /etc/nginx/sites-available/gautamsingh
sudo ln -sf /etc/nginx/sites-available/gautamsingh /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl restart nginx

echo ""
echo "═══════════════════════════════════════════════"
echo "  ✅ Deployment Complete!"
echo "═══════════════════════════════════════════════"
echo ""
echo "  Your website should be live at:"
echo "  http://YOUR_EC2_PUBLIC_IP"
echo ""
echo "  Next steps:"
echo "  1. Edit .env → nano /home/ubuntu/Gautamsinghmodle/.env"
echo "  2. Set DJANGO_ALLOWED_HOSTS to your EC2 IP"
echo "  3. Update Nginx config with your IP:"
echo "     sudo nano /etc/nginx/sites-available/gautamsingh"
echo "  4. Restart services:"
echo "     sudo systemctl restart gunicorn nginx"
echo "  5. Create admin user:"
echo "     cd /home/ubuntu/Gautamsinghmodle"
echo "     source venv/bin/activate"
echo "     python3 manage.py createsuperuser"
echo ""
