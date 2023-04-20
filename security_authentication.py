# pip install pynacl PyJWT

import nacl.utils
from nacl.public import PrivateKey, PublicKey, Box
import jwt
import time

class Security:
    def __init__(self, private_key=None):
        if private_key:
            self.private_key = private_key
        else:
            self.private_key = PrivateKey.generate()

        self.public_key = self.private_key.public_key

    def encrypt_message(self, recipient_public_key, message):
        box = Box(self.private_key, recipient_public_key)
        encrypted_message = box.encrypt(message)
        return encrypted_message

    def decrypt_message(self, sender_public_key, encrypted_message):
        box = Box(self.private_key, sender_public_key)
        decrypted_message = box.decrypt(encrypted_message)
        return decrypted_message

class Authentication:
    def __init__(self, secret_key):
        self.secret_key = secret_key

    def generate_jwt(self, drone_id, expiry_duration=3600):
        payload = {
            'drone_id': drone_id,
            'exp': time.time() + expiry_duration
        }
        token = jwt.encode(payload, self.secret_key, algorithm='HS256')
        return token

    def decode_jwt(self, token):
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=['HS256'])
            return payload
        except jwt.ExpiredSignatureError:
            raise ValueError("Token expired")
        except jwt.InvalidTokenError:
            raise ValueError("Invalid token")
