import bcrypt


class PasswordManager:
    @staticmethod
    def get_password_hash(password: str) -> bytes:
        return bcrypt.hashpw(password=password.encode(), salt=bcrypt.gensalt())

    @staticmethod
    def check_password_hash(password: str, hashed: bytes) -> bool:
        return bcrypt.checkpw(
            password=password.encode(), hashed_password=hashed.encode()
        )
