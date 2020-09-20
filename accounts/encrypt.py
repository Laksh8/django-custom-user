from cryptography.fernet import Fernet
from django.conf import settings


# def generate_key():
#     """
#     Generates a key and save it into a file
#     """
#     key = Fernet.generate_key()
#     with open(str(settings.BASE_DIR)+"/accounts/secret.key", "wb") as key_file:
#         key_file.write(key)

def load_key():
    """
    Load the previously generated key
    """
    return open(str(settings.BASE_DIR)+"/accounts/secret.key", "rb").read()

def encrypt_message(message):
    """
    Encrypts a message
    """
    key = load_key()
    encoded_message = str(message).encode()
    f = Fernet(key)
    encrypted_message = f.encrypt(encoded_message)

    return encrypted_message.decode()

def decrypt_message(encrypted_message):
    """
    Decrypts an encrypted message
    """
    key = load_key()
    f = Fernet(key)
    decrypted_message = f.decrypt(encrypted_message.encode())

    return decrypted_message.decode()