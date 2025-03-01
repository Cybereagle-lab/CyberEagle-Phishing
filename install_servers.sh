#!/bin/bash

# Install Ngrok
echo "Installing Ngrok..."
if ! command -v ngrok &> /dev/null; then
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        sudo snap install ngrok
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        brew install ngrok/ngrok/ngrok
    else
        echo "Unsupported OS for Ngrok installation. Please install manually from https://ngrok.com/download."
    fi
else
    echo "Ngrok is already installed."
fi

# Install LocalTunnel
echo "Installing LocalTunnel..."
if ! command -v lt &> /dev/null; then
    npm install -g localtunnel
else
    echo "LocalTunnel is already installed."
fi

# Install PageKite
echo "Installing PageKite..."
if ! command -v pagekite.py &> /dev/null; then
    pip install pagekite
else
    echo "PageKite is already installed."
fi

# Install LocalXpose
echo "Installing LocalXpose..."
if ! command -v loclx &> /dev/null; then
    echo "Please download LocalXpose from https://localxpose.io/download and install manually."
else
    echo "LocalXpose is already installed."
fi

# Install Cloudflare Tunnel
echo "Installing Cloudflare Tunnel..."
if ! command -v cloudflared &> /dev/null; then
    echo "Please download Cloudflare Tunnel from https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/install-and-setup/installation and install manually."
else
    echo "Cloudflare Tunnel is already installed."
fi

echo "All server tools installed successfully!"
