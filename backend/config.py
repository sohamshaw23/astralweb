import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "zenith-secret-key-98213")
    DEBUG = True
