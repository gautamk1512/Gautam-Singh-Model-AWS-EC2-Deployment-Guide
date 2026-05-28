#!/bin/bash
# ═══════════════════════════════════════════════════════════
# AWS Deployment Helper Script for Gautam Singh Model
# This script helps automate the AWS deployment process
# ═══════════════════════════════════════════════════════════

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if AWS CLI is installed
check_aws_cli() {
    if ! command -v aws &> /dev/null; then
        print_error "AWS CLI is not installed. Please install it first."
        echo "Install from: https://aws.amazon.com/cli/"
        exit 1
    fi
    print_success "AWS CLI is installed"
}

# Function to check AWS credentials
check_aws_credentials() {
    print_status "Checking AWS credentials..."
    if aws sts get-caller-identity &> /dev/null; then
        print_success "AWS credentials are valid"
        ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
        print_status "AWS Account ID: $ACCOUNT_ID"
    else
        print_error "AWS credentials are not valid or not configured"
        echo "Run: aws configure"
        exit 1
    fi
}

# Function to create EC2 instance
create_ec2_instance() {
    print_status "Creating EC2 instance..."
    
    # Get user input
    read -p "Enter instance name (default: gautam-singh-model): " INSTANCE_NAME
    INSTANCE_NAME=${INSTANCE_NAME:-gautam-singh-model}
    
    read -p "Enter instance type (default: t2.micro): " INSTANCE_TYPE
    INSTANCE_TYPE=${INSTANCE_TYPE:-t2.micro}
    
    read -p "Enter key pair name: " KEY_PAIR
    if [ -z "$KEY_PAIR" ]; then
        print_error "Key pair name is required"
        exit 1
    fi
    
    # Create security group
    print_status "Creating security group..."
    SECURITY_GROUP_ID=$(aws ec2 create-security-group \
        --group-name "gautam-singh-model-sg" \
        --description "Security group for Gautam Singh Model trading platform" \
        --query GroupId --output text 2>/dev/null || \
        aws ec2 describe-security-groups \
        --group-names "gautam-singh-model-sg" \
        --query SecurityGroups[0].GroupId --output text)
    
    # Add security group rules
    print_status "Configuring security group rules..."
    aws ec2 authorize-security-group-ingress \
        --group-id $SECURITY_GROUP_ID \
        --protocol tcp --port 22 --cidr 0.0.0.0/0 2>/dev/null || true
    
    aws ec2 authorize-security-group-ingress \
        --group-id $SECURITY_GROUP_ID \
        --protocol tcp --port 80 --cidr 0.0.0.0/0 2>/dev/null || true
    
    aws ec2 authorize-security-group-ingress \
        --group-id $SECURITY_GROUP_ID \
        --protocol tcp --port 443 --cidr 0.0.0.0/0 2>/dev/null || true
    
    # Get latest Ubuntu AMI
    print_status "Getting latest Ubuntu AMI..."
    AMI_ID=$(aws ec2 describe-images \
        --owners 099720109477 \
        --filters "Name=name,Values=ubuntu/images/hvm-ssd/ubuntu-24.04-amd64-server-*" \
        --query 'Images | sort_by(@, &CreationDate) | [-1].ImageId' \
        --output text)
    
    print_status "Using AMI: $AMI_ID"
    
    # Create EC2 instance
    print_status "Creating EC2 instance..."
    INSTANCE_ID=$(aws ec2 run-instances \
        --image-id $AMI_ID \
        --instance-type $INSTANCE_TYPE \
        --key-name $KEY_PAIR \
        --security-group-ids $SECURITY_GROUP_ID \
        --tag-specifications "ResourceType=instance,Tags=[{Key=Name,Value=$INSTANCE_NAME}]" \
        --query Instances[0].InstanceId --output text)
    
    print_success "EC2 instance created: $INSTANCE_ID"
    
    # Wait for instance to be running
    print_status "Waiting for instance to be running..."
    aws ec2 wait instance-running --instance-ids $INSTANCE_ID
    
    # Get public IP
    PUBLIC_IP=$(aws ec2 describe-instances \
        --instance-ids $INSTANCE_ID \
        --query Reservations[0].Instances[0].PublicIpAddress \
        --output text)
    
    print_success "Instance is running at: $PUBLIC_IP"
    
    # Save instance details
    echo "INSTANCE_ID=$INSTANCE_ID" > deploy/aws_instance_info.txt
    echo "PUBLIC_IP=$PUBLIC_IP" >> deploy/aws_instance_info.txt
    echo "SECURITY_GROUP_ID=$SECURITY_GROUP_ID" >> deploy/aws_instance_info.txt
    echo "INSTANCE_NAME=$INSTANCE_NAME" >> deploy/aws_instance_info.txt
}

# Function to create Elastic IP
create_elastic_ip() {
    print_status "Creating Elastic IP..."
    ALLOCATION_ID=$(aws ec2 allocate-address --domain vpc --query AllocationId --output text)
    
    # Get instance ID from saved file
    if [ -f deploy/aws_instance_info.txt ]; then
        source deploy/aws_instance_info.txt
        aws ec2 associate-address --instance-id $INSTANCE_ID --allocation-id $ALLOCATION_ID
        print_success "Elastic IP created and associated"
        
        # Get the elastic IP
        ELASTIC_IP=$(aws ec2 describe-addresses --allocation-ids $ALLOCATION_ID --query Addresses[0].PublicIp --output text)
        echo "ELASTIC_IP=$ELASTIC_IP" >> deploy/aws_instance_info.txt
        print_success "Elastic IP: $ELASTIC_IP"
    else
        print_warning "Instance info not found. Please create instance first."
    fi
}

# Function to deploy application
deploy_application() {
    print_status "Deploying application..."
    
    if [ -f deploy/aws_instance_info.txt ]; then
        source deploy/aws_instance_info.txt
        
        print_status "Uploading project to EC2 instance..."
        
        # Get key pair path
        read -p "Enter path to your .pem key file: " KEY_PATH
        if [ ! -f "$KEY_PATH" ]; then
            print_error "Key file not found: $KEY_PATH"
            exit 1
        fi
        
        # Set correct permissions for key
        chmod 400 $KEY_PATH
        
        # Upload project
        print_status "Uploading project files..."
        scp -i $KEY_PATH -r . ubuntu@$PUBLIC_IP:/home/ubuntu/
        
        # Run deployment script on remote server
        print_status "Running deployment script on remote server..."
        ssh -i $KEY_PATH ubuntu@$PUBLIC_IP << 'ENDSSH'
            cd /home/ubuntu/Gautamsinghmodle
            chmod +x deploy/setup_server.sh
            bash deploy/setup_server.sh
ENDSSH
        
        print_success "Application deployed successfully!"
        print_success "Access your site at: http://$PUBLIC_IP"
        
    else
        print_error "Instance info not found. Please create instance first."
        exit 1
    fi
}

# Function to setup SSL
setup_ssl() {
    print_status "Setting up SSL certificate..."
    
    if [ -f deploy/aws_instance_info.txt ]; then
        source deploy/aws_instance_info.txt
        
        read -p "Enter your domain name (e.g., yourdomain.com): " DOMAIN
        
        # Get key pair path
        read -p "Enter path to your .pem key file: " KEY_PATH
        chmod 400 $KEY_PATH
        
        # Install certbot and setup SSL
        ssh -i $KEY_PATH ubuntu@$PUBLIC_IP << ENDSSH
            sudo apt update
            sudo apt install -y certbot python3-certbot-nginx
            sudo certbot --nginx -d $DOMAIN --non-interactive --agree-tos -m admin@$DOMAIN
ENDSSH
        
        print_success "SSL certificate installed successfully!"
        print_success "Access your secure site at: https://$DOMAIN"
        
    else
        print_error "Instance info not found. Please create instance first."
        exit 1
    fi
}

# Function to show status
show_status() {
    if [ -f deploy/aws_instance_info.txt ]; then
        source deploy/aws_instance_info.txt
        print_status "AWS Instance Status:"
        echo "  Instance ID: $INSTANCE_ID"
        echo "  Public IP: $PUBLIC_IP"
        echo "  Instance Name: $INSTANCE_NAME"
        if [ ! -z "$ELASTIC_IP" ]; then
            echo "  Elastic IP: $ELASTIC_IP"
        fi
        echo "  Security Group ID: $SECURITY_GROUP_ID"
    else
        print_warning "No instance information found."
    fi
}

# Function to cleanup resources
cleanup() {
    print_warning "This will delete all AWS resources created by this script."
    read -p "Are you sure? (yes/no): " CONFIRM
    
    if [ "$CONFIRM" = "yes" ]; then
        if [ -f deploy/aws_instance_info.txt ]; then
            source deploy/aws_instance_info.txt
            
            print_status "Terminating EC2 instance..."
            aws ec2 terminate-instances --instance-ids $INSTANCE_ID
            
            print_status "Releasing Elastic IP..."
            if [ ! -z "$ELASTIC_IP" ]; then
                ALLOCATION_ID=$(aws ec2 describe-addresses --public-ips $ELASTIC_IP --query Addresses[0].AllocationId --output text)
                aws ec2 release-address --allocation-id $ALLOCATION_ID
            fi
            
            print_status "Deleting security group..."
            aws ec2 delete-security-group --group-id $SECURITY_GROUP_ID
            
            rm -f deploy/aws_instance_info.txt
            print_success "Cleanup completed!"
        else
            print_warning "No resources to cleanup."
        fi
    else
        print_status "Cleanup cancelled."
    fi
}

# Main menu
show_menu() {
    echo ""
    echo "═══════════════════════════════════════════════════"
    echo "  Gautam Singh Model - AWS Deployment Helper"
    echo "═══════════════════════════════════════════════════"
    echo ""
    echo "1. Check AWS Setup"
    echo "2. Create EC2 Instance"
    echo "3. Create Elastic IP"
    echo "4. Deploy Application"
    echo "5. Setup SSL Certificate"
    echo "6. Show Status"
    echo "7. Cleanup Resources"
    echo "8. Exit"
    echo ""
}

# Main function
main() {
    # Create deploy directory if it doesn't exist
    mkdir -p deploy
    
    while true; do
        show_menu
        read -p "Select an option (1-8): " CHOICE
        
        case $CHOICE in
            1)
                check_aws_cli
                check_aws_credentials
                ;;
            2)
                check_aws_cli
                check_aws_credentials
                create_ec2_instance
                ;;
            3)
                create_elastic_ip
                ;;
            4)
                check_aws_cli
                check_aws_credentials
                deploy_application
                ;;
            5)
                setup_ssl
                ;;
            6)
                show_status
                ;;
            7)
                cleanup
                ;;
            8)
                print_success "Goodbye!"
                exit 0
                ;;
            *)
                print_error "Invalid option. Please select 1-8."
                ;;
        esac
        
        echo ""
        read -p "Press Enter to continue..."
    done
}

# Run main function
main "$@"