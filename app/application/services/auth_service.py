from passlib.hash import bcrypt #strong password hashing

class AuthService:
    def hash_password(self, plain_password): #Hashes the plain text password.
        return bcrypt.hash(plain_password)
    
    def verify_password(self, plain_password, hashed_password): #Verifies a password by comparing it to a stored hash.
        return bcrypt.verify(plain_password, hashed_password)