import base64
import bcrypt

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from config import Config, load_config


class SecureEncryptor:

    def __init__(self, user_id: int):

        self.user_id = user_id
        self.config: Config = load_config()

    def encrypt_data(self, data: str) -> str:

        cipher = self._generate_cipher()
        encrypted = cipher.encrypt(data.encode())

        return encrypted.decode()

    def decrypted_data(self, data: str) -> str:

        cipher = self._generate_cipher()
        decrypted = cipher.decrypt(data.encode())

        return decrypted.decode()

    def _generate_cipher(self):

        salt = str(self.user_id)
        secret_key: str = self.config.secret_key.SECRET_KEY

        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt.encode(),
            iterations=390000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(secret_key.encode()))

        return Fernet(key)

    def generate_hash_str(self, password: str) -> str:

        password_bytes: bytes = password.encode("utf-8")
        password_salt: bytes = bcrypt.gensalt()
        hash_bytes: bytes = bcrypt.hashpw(password_bytes, password_salt)
        hash_str: str = hash_bytes.decode("utf-8")

        return hash_str

    def authenticate(self, password: str, hash_str: str) -> bool:

        password_bytes: bytes = password.encode("utf-8")
        hash_bytes: bytes = hash_str.encode("utf-8")
        result: bool = bcrypt.checkpw(password_bytes, hash_bytes)

        return result
