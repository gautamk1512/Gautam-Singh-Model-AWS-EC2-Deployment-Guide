# ═══════════════════════════════════════════════════════════
# AWS CLI Setup and Deployment Guide
# ═══════════════════════════════════════════════════════════

## 🚀 Quick Start - AWS CLI Installation

### Windows (PowerShell - Run as Administrator)
```powershell
# Download and install AWS CLI
msiexec.exe /i https://awscli.amazonaws.com/AWSCLIV2.msi

# Verify installation
aws --version

# Configure AWS CLI
aws configure
```

### macOS
```bash
# Install using Homebrew
brew install awscli

# Or download installer
curl "https://awscli.amazonaws.com/AWSCLIV2.pkg" -o "AWSCLIV2.pkg"
sudo installer -pkg AWSCLIV2.pkg -target /

# Verify installation
aws --version

# Configure AWS CLI
aws configure
```

### Linux (Ubuntu/Debian)
```bash
# Install AWS CLI
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install

# Verify installation
aws --version

# Configure AWS CLI
aws configure
```

## 🔑 AWS Configuration

### Get your AWS credentials:
1. Log into AWS Console: https://console.aws.amazon.com
2. Go to: IAM → Users → [Your User] → Security credentials
3. Click "Create access key"
4. Save your Access Key ID and Secret Access Key

### Configure AWS CLI:
```bash
aws configure
# Enter your Access Key ID
# Enter your Secret Access Key
# Enter your region (e.g., us-east-1, ap-southeast-2)
# Enter output format (json)
```

### Test your configuration:
```bash
# Check your identity
aws sts get-caller-identity

# List EC2 instances
aws ec2 describe-instances --query Reservations[*].Instances[*].[InstanceId,State.Name,PublicIpAddress] --output table
```

## 🏗️ AWS Services Setup

### 1. Create IAM User (Recommended)
```bash
# Create IAM user for deployment
aws iam create-user --user-name gautam-singh-deploy

# Attach necessary policies
aws iam attach-user-policy --user-name gautam-singh-deploy --policy-arn arn:aws:iam::aws:policy/AmazonEC2FullAccess
aws iam attach-user-policy --user-name gautam-singh-deploy --policy-arn arn:aws:iam::aws:policy/AmazonRoute53FullAccess

# Create access keys for the new user
aws iam create-access-key --user-name gautam-singh-deploy
```

### 2. Create Key Pair
```bash
# Create EC2 key pair
aws ec2 create-key-pair --key-name gautam-singh-keypair --query 'KeyMaterial' --output text > gautam-singh-keypair.pem

# Set correct permissions
chmod 400 gautam-singh-keypair.pem
```

### 3. Create Security Group
```bash
# Create security group
aws ec2 create-security-group \
    --group-name gautam-singh-model-sg \
    --description "Security group for Gautam Singh Model trading platform"

# Add rules
aws ec2 authorize-security-group-ingress \
    --group-name gautam-singh-model-sg \
    --protocol tcp --port 22 --cidr 0.0.0.0/0

aws ec2 authorize-security-group-ingress \
    --group-name gautam-singh-model-sg \
    --protocol tcp --port 80 --cidr 0.0.0.0/0

aws ec2 authorize-security-group-ingress \
    --group-name gautam-singh-model-sg \
    --protocol tcp --port 443 --cidr 0.0.0.0/0
```

### 4. Launch EC2 Instance
```bash
# Get latest Ubuntu AMI
AMI_ID=$(aws ec2 describe-images \
    --owners 099720109477 \
    --filters "Name=name,Values=ubuntu/images/hvm-ssd/ubuntu-24.04-amd64-server-*" \
    --query 'Images | sort_by(@, &CreationDate) | [-1].ImageId' \
    --output text)

# Launch instance
aws ec2 run-instances \
    --image-id $AMI_ID \
    --instance-type t2.micro \
    --key-name gautam-singh-keypair \
    --security-groups gautam-singh-model-sg \
    --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=gautam-singh-model}]'

# Get instance ID and wait for it to be running
INSTANCE_ID=$(aws ec2 describe-instances \
    --filters "Name=tag:Name,Values=gautam-singh-model" \
    --query 'Reservations[-1].Instances[0].InstanceId' \
    --output text)

aws ec2 wait instance-running --instance-ids $INSTANCE_ID

# Get public IP
PUBLIC_IP=$(aws ec2 describe-instances \
    --instance-ids $INSTANCE_ID \
    --query 'Reservations[0].Instances[0].PublicIpAddress' \
    --output text)

echo "Instance is running at: $PUBLIC_IP"
```

## 🚀 Deployment Commands

### Connect to your instance:
```bash
ssh -i gautam-singh-keypair.pem ubuntu@$PUBLIC_IP
```

### Upload your project:
```bash
# From your local machine
scp -i gautam-singh-keypair.pem -r ./Gautamsinghmodle ubuntu@$PUBLIC_IP:/home/ubuntu/
```

### Deploy on the server:
```bash
# On the EC2 instance
cd /home/ubuntu/Gautamsinghmodle
chmod +x deploy/setup_server.sh
bash deploy/setup_server.sh
```

## 🔒 SSL Certificate Setup

### Install Certbot:
```bash
# On the EC2 instance
sudo apt update
sudo apt install -y certbot python3-certbot-nginx
```

### Get SSL certificate:
```bash
# Replace with your domain
sudo certbot --nginx -d yourdomain.com --non-interactive --agree-tos -m admin@yourdomain.com
```

## 📊 Monitoring Commands

### Check instance status:
```bash
aws ec2 describe-instance-status --instance-ids $INSTANCE_ID
```

### View system logs:
```bash
# On the EC2 instance
sudo journalctl -u gunicorn -f
sudo tail -f /var/log/nginx/error.log
```

### Monitor resources:
```bash
# Check CPU and memory usage
top
htop

# Check disk usage
df -h

# Check network connections
netstat -tulpn
```

## 🧹 Cleanup Commands

### Terminate instance:
```bash
aws ec2 terminate-instances --instance-ids $INSTANCE_ID
```

### Delete security group:
```bash
aws ec2 delete-security-group --group-name gautam-singh-model-sg
```

### Delete key pair:
```bash
aws ec2 delete-key-pair --key-name gautam-singh-keypair
rm -f gautam-singh-keypair.pem
```

## 🛠️ Troubleshooting

### Common Issues:

1. **AWS CLI not working:**
   - Check if AWS CLI is installed: `aws --version`
   - Verify credentials: `aws sts get-caller-identity`
   - Check region configuration: `aws configure get region`

2. **Instance connection issues:**
   - Check security group rules
   - Verify key pair permissions (chmod 400)
   - Check instance state: `aws ec2 describe-instances --instance-ids $INSTANCE_ID`

3. **Deployment issues:**
   - Check Django logs: `sudo journalctl -u gunicorn -f`
   - Check Nginx logs: `sudo tail -f /var/log/nginx/error.log`
   - Verify .env file configuration

4. **SSL certificate issues:**
   - Check domain DNS settings
   - Verify port 80 is open for HTTP challenge
   - Check certificate expiration: `sudo certbot certificates`

## 📞 Support

If you encounter issues:
1. Check AWS documentation: https://docs.aws.amazon.com/
2. Review deployment logs
3. Verify all configurations
4. Test each step individually