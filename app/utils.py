from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash(password):
    return pwd_context.encrypt(password)


def verify(passwordAttempt, userPassword):
    return pwd_context.verify(passwordAttempt, userPassword)
