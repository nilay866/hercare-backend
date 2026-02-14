#!/bin/bash
set -e

echo "Installing Nginx..."
sudo dnf install -y nginx

echo "Configuring Nginx..."
sudo cp /home/ec2-user/nginx.conf /etc/nginx/nginx.conf

echo "Starting Nginx..."
sudo systemctl enable nginx
sudo systemctl restart nginx

echo "Nginx Setup Complete!"
