import os
import base64
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet

PASSWORD_FILE = os.path.expanduser("~/Soap/secrets/email_app_pass.txt")  # Contains Jenco610##
SALT_FILE = os.path.expanduser("~/Soap/secrets/overlay.salt")

def get_password():
    with open(PASSWORD_FILE, "r") as f:
        return f.read().strip().encode()

def get_salt():
    if os.path.isfile(SALT_FILE):
        with open(SALT_FILE, "rb") as f:
            return f.read()
    salt = os.urandom(16)
    with open(SALT_FILE, "wb") as f:
        f.write(salt)
    return salt

def derive_key(password, salt):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100_000,
        backend=default_backend()
    )
    return base64.urlsafe_b64encode(kdf.derive(password))

def encrypt_overlay(filename):
    overlay = os.path.expanduser("~/Soap/overlay")
    path = os.path.join(overlay, filename)
    password = get_password()
    salt = get_salt()
    key = derive_key(password, salt)
    f = Fernet(key)
    with open(path, "rb") as file:
        encrypted = f.encrypt(file.read())
    with open(path + ".enc", "wb") as file:
        file.write(encrypted)
    print(f"Encrypted {filename} to {filename}.enc using password.")

def decrypt_overlay(enc_filename):
    overlay = os.path.expanduser("~/Soap/overlay")
    path = os.path.join(overlay, enc_filename)
    password = get_password()
    salt = get_salt()
    key = derive_key(password, salt)
    f = Fernet(key)
    with open(path, "rb") as file:
        decrypted = f.decrypt(file.read())
    out_path = path.replace(".enc", "")
    with open(out_path, "wb") as file:
        file.write(decrypted)
    print(f"Decrypted {enc_filename} to {os.path.basename(out_path)} using password.")

if __name__ == "__main__":
    import sys
    if len(sys.argv) == 3:
        if sys.argv[1] == "encrypt":
            encrypt_overlay(sys.argv[2])
        elif sys.argv[1] == "decrypt":
            decrypt_overlay(sys.argv[2])
        else:
            print("Use: encrypt <filename> OR decrypt <encrypted_filename>")
    else:
        print("Usage: python rotor_overlay_encrypt.py encrypt <filename>")
        print("       python rotor_overlay_encrypt.py decrypt <filename.enc>")
