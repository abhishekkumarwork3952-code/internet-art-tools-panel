#!/bin/bash

# Internet Art Tools - Deployment Script for EC2

echo "Starting deployment..."

# Update system
sudo apt update

# Install Python and pip
sudo apt install -y python3 python3-pip python3-venv

# Install Nginx
sudo apt install -y nginx

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --noinput

# Run migrations
python manage.py migrate

# Create superuser (optional - comment out if not needed)
# python manage.py createsuperuser

# Setup Nginx configuration
sudo cp nginx.conf /etc/nginx/sites-available/internet-art-tools
sudo ln -sf /etc/nginx/sites-available/internet-art-tools /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

# Test Nginx configuration
sudo nginx -t

# Restart Nginx
sudo systemctl restart nginx
sudo systemctl enable nginx

# Setup systemd service
sudo cp internet-art-tools.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable internet-art-tools
sudo systemctl start internet-art-tools

echo "Deployment completed!"
echo "Your application should be running on http://your-ec2-ip"
