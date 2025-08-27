# Snakeware
Snakeware is a python-based proof-of-concept ransomware designed to demonstrate encryption and recovery concepts in a safe setting. It is NOT intended for usage as operational software, and should not be used outside of a controlled environment.

# What It Does
Snakeware, when run as an executable file, will produce a snake game for the user to play. Playing this game will cause the software to encrypt all files in Desktop/Test using AES-CBC, before using RSA to encrypt and send the symmetric key to the 'attacker'.
