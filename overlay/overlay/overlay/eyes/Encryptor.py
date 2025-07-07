#!/usr/bin/env python3
from cryptography.fernet import Fernet
from core.rotor_overlay import log_event

def encrypt_file(file_path, key):
    with open(file_path, 'rb') as file:
        data = file.read()

    fernet = Fernet(key)
    encrypted_data = fernet.encrypt(data)

    with open(file_path + '.enc', 'wb') as file:
        file.write(encrypted_data)

    log_event("ENCRYPTOR", f"File encrypted successfully: {file_path}.enc")
