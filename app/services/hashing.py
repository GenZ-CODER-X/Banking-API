from passlib.context import CryptContext
pwd_context=CryptContext(schemes=["bcrypt"],deprecated="auto") 
def hash_password(password:str):
    return pwd_context.hash(password)

def verify(plainpassword,storedpassword):
    return pwd_context.verify(plainpassword,storedpassword)