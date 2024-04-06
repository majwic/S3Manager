from cryptography.fernet import Fernet
import hashlib
import base64

def generate_fernet_key(password):
    hashed_password = hashlib.sha256(password.encode()).digest()
    fernet_key = hashed_password[:32]
    return base64.urlsafe_b64encode(fernet_key)

def encrypt_file(file_path, password, encrypted_file_path):
    with open(file_path, 'rb') as f:
        data = f.read()

    key = generate_fernet_key(password)
    cipher_suite = Fernet(key)
    encrypted_data = cipher_suite.encrypt(data)

    with open(encrypted_file_path, 'wb') as f:
        f.write(encrypted_data)
    
    return encrypted_file_path

def decrypt_file(encrypted_file_path, password):
    with open(encrypted_file_path, 'rb') as f:
        encrypted_data = f.read()

    key = generate_fernet_key(password)
    cipher_suite = Fernet(key)
    try: 
        decrypted_data = cipher_suite.decrypt(encrypted_data)
    except Exception:
        return
    
    with open(encrypted_file_path, 'wb') as f:
        f.write(decrypted_data)