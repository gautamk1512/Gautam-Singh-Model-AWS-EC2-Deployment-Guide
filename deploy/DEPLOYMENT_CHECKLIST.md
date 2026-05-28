# ═══════════════════════════════════════════════════════════
# AWS Deployment Checklist for Gautam Singh Model
# ═══════════════════════════════════════════════════════════

## 📋 Pre-Deployment Checklist

### ✅ AWS Account Setup
- [ ] AWS account created and verified
- [ ] Payment method added to AWS account
- [ ] IAM user created with appropriate permissions
- [ ] Access keys generated and saved securely

### ✅ Local Environment Setup
- [ ] AWS CLI installed on local machine
- [ ] AWS CLI configured with credentials
- [ ] SSH key pair created (or existing one identified)
- [ ] Project files ready for deployment
- [ ] All dependencies installed locally

### ✅ Application Configuration
- [ ] Environment variables configured (.env file)
- [ ] Database migrations tested locally
- [ ] Static files collection working
- [ ] Application running successfully on localhost
- [ ] All features tested (login, payments, indicators)

---

## 🚀 Deployment Steps

### Step 1: AWS Infrastructure Setup
```bash
# Run the deployment helper script
chmod +x deploy/aws_deploy_helper.sh
bash deploy/aws_deploy_helper.sh
```

**Manual Steps if not using helper script:**
- [ ] Create EC2 security group
- [ ] Configure security group rules (SSH, HTTP, HTTPS)
- [ ] Launch EC2 instance (Ubuntu 24.04 LTS)
- [ ] Create Elastic IP and associate with instance
- [ ] Note down public IP address

### Step 2: Server Configuration
- [ ] Connect to EC2 instance via SSH
- [ ] Update system packages
- [ ] Install required software (Python, Nginx, Git)
- [ ] Configure firewall (UFW)
- [ ] Set up time zone

### Step 3: Application Deployment
- [ ] Upload project files to server
- [ ] Create Python virtual environment
- [ ] Install Python dependencies
- [ ] Configure environment variables
- [ ] Run database migrations
- [ ] Collect static files
- [ ] Test Django application

### Step 4: Web Server Setup
- [ ] Configure Gunicorn service
- [ ] Set up Nginx reverse proxy
- [ ] Configure Nginx for static files
- [ ] Test web server configuration
- [ ] Enable and start services

### Step 5: SSL Certificate (Optional but Recommended)
- [ ] Install Certbot
- [ ] Obtain SSL certificate
- [ ] Configure automatic renewal
- [ ] Test HTTPS access

### Step 6: Domain Setup (Optional)
- [ ] Purchase domain name
- [ ] Configure DNS A record to point to EC2 IP
- [ ] Update Django settings with domain
- [ ] Test domain access

---

## 🔧 Post-Deployment Checklist

### ✅ Application Testing
- [ ] Access application via public IP
- [ ] Test all pages load correctly
- [ ] Verify database connectivity
- [ ] Test user registration/login
- [ ] Test payment integration (demo mode)
- [ ] Test indicator purchase flow
- [ ] Verify email functionality
- [ ] Test admin panel access

### ✅ Performance Optimization
- [ ] Enable Gzip compression
- [ ] Configure browser caching
- [ ] Optimize database queries
- [ ] Set up CDN for static files (optional)
- [ ] Configure log rotation

### ✅ Security Hardening
- [ ] Change default passwords
- [ ] Disable root SSH login
- [ ] Configure fail2ban
- [ ] Set up automated security updates
- [ ] Configure backup strategy
- [ ] Review and update security group rules

### ✅ Monitoring Setup
- [ ] Set up CloudWatch monitoring
- [ ] Configure disk space alerts
- [ ] Set up CPU/memory monitoring
- [ ] Configure log aggregation
- [ ] Test alert notifications

---

## 📊 AWS Services Configuration

### EC2 Instance Settings
```bash
# Recommended instance settings
INSTANCE_TYPE="t2.micro"          # Free tier eligible
AMI="ubuntu-24.04-lts"           # Latest Ubuntu
SECURITY_GROUP="gautam-singh-model-sg"
KEY_PAIR="gautam-singh-keypair"
```

### Security Group Rules
```bash
# SSH Access (restrict to your IP if possible)
aws ec2 authorize-security-group-ingress \
    --group-name gautam-singh-model-sg \
    --protocol tcp --port 22 --cidr YOUR_IP/32

# HTTP Access
aws ec2 authorize-security-group-ingress \
    --group-name gautam-singh-model-sg \
    --protocol tcp --port 80 --cidr 0.0.0.0/0

# HTTPS Access
aws ec2 authorize-security-group-ingress \
    --group-name gautam-singh-model-sg \
    --protocol tcp --port 443 --cidr 0.0.0.0/0
```

---

## 🚨 Troubleshooting Guide

### Common Issues and Solutions

#### 1. Cannot Connect to EC2 Instance
- [ ] Check security group rules
- [ ] Verify key pair permissions (chmod 400)
- [ ] Check instance state (running?)
- [ ] Verify public IP address

#### 2. Application Not Loading
- [ ] Check Gunicorn service status
- [ ] Check Nginx configuration
- [ ] Verify static files collection
- [ ] Check Django logs

#### 3. Database Connection Issues
- [ ] Verify database migrations
- [ ] Check database permissions
- [ ] Verify database connection settings
- [ ] Check for database corruption

#### 4. SSL Certificate Issues
- [ ] Check domain DNS settings
- [ ] Verify port 80 accessibility
- [ ] Check certificate expiration
- [ ] Review Certbot logs

#### 5. Performance Issues
- [ ] Monitor CPU and memory usage
- [ ] Check disk space availability
- [ ] Review application logs for errors
- [ ] Analyze database query performance

---

## 📞 Emergency Contacts and Resources

### AWS Support
- AWS Support Center: https://console.aws.amazon.com/support/
- AWS Documentation: https://docs.aws.amazon.com/
- AWS Forums: https://forums.aws.amazon.com/

### Application Support
- Django Documentation: https://docs.djangoproject.com/
- Nginx Documentation: https://nginx.org/en/docs/
- Gunicorn Documentation: https://docs.gunicorn.org/

### Monitoring Tools
- AWS CloudWatch: https://console.aws.amazon.com/cloudwatch/
- System logs: `/var/log/` directory
- Application logs: Check your Django logs

---

## 🔄 Maintenance Checklist

### Daily Tasks
- [ ] Check application availability
- [ ] Monitor error logs
- [ ] Verify backup completion
- [ ] Check SSL certificate status

### Weekly Tasks
- [ ] Review security logs
- [ ] Check disk space usage
- [ ] Monitor performance metrics
- [ ] Update system packages

### Monthly Tasks
- [ ] Review AWS billing
- [ ] Update application dependencies
- [ ] Test disaster recovery procedures
- [ ] Review and update documentation

---

## 🎯 Success Criteria

### Deployment is Successful When:
- [ ] Application loads without errors
- [ ] All features work as expected
- [ ] Performance is acceptable
- [ ] Security measures are in place
- [ ] Monitoring is configured
- [ ] Documentation is complete

### Ready for Production When:
- [ ] Load testing completed
- [ ] Security audit passed
- [ ] Backup strategy tested
- [ ] Disaster recovery plan tested
- [ ] Performance benchmarks met
- [ ] Team training completed