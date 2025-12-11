#!/bin/bash

# Ethical Hacker Scanning Tool - Setup Script
# Installs all necessary packages for network and security scanning

set -e

echo "Installing required packages for Ethical Hacker Scanning Tool..."

# Update package list
sudo apt update

# Core scanning tools
echo "Installing core scanning tools..."
sudo apt install -y nmap
sudo apt install -y dirb
sudo apt install -y sqlmap

# Additional useful tools
echo "Installing additional scanning and utility tools..."
sudo apt install -y nikto          # Web server vulnerability scanner
sudo apt install -y masscan        # Fast network port scanner
sudo apt install -y netcat         # Network utility for reading/writing data
sudo apt install -y curl           # Data transfer tool
sudo apt install -y wget           # File retrieval tool
sudo apt install -y whois          # WHOIS lookup utility
sudo apt install -y dnsutils       # DNS query tools
sudo apt install -y hydra          # Brute force tool
sudo apt install -y hashcat        # Password cracking tool

# # Python dependencies
# echo "Installing Python dependencies..."
# sudo apt install -y python3-pip
# pip3 install --upgrade pip
# pip3 install requests
# pip3 install beautifulsoup4
# pip3 install python-nmap
# pip3 install dnspython

echo "Setup complete! All required packages have been installed."