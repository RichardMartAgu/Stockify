from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Hash:

    def hash_password(self):
        return pwd_context.hash(self)

    def verify_password(self, hashed_password):
        return pwd_context.verify(self, hashed_password)
