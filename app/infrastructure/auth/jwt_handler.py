# import jwt
# from datetime import datetime, timedelta
# import os

# SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-secret-key")
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 60  # 1 hour

# class JWTHandler:
#     def create_token(self, user_id: str, role: str):
#         expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#         payload = {
#             "sub": user_id,
#             "role": role,
#             "exp": expire
#         }
#         token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
#         return token

#     def decode_token(self, token: str):
#         try:
#             payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#             return payload
#         except jwt.ExpiredSignatureError:
#             raise Exception("Token expired")
#         except jwt.InvalidTokenError:
#             raise Exception("Invalid token")
