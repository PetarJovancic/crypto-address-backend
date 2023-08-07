import os
from dotenv import load_dotenv


load_dotenv()


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    JWT_ACCESS_TOKEN_EXPIRES = 6000
    JWT_ALGORITHM = os.getenv('JWT_ALGORITHM')
    WALLET_LANGUAGE = os.getenv('WALLET_LANGUAGE')
    WALLET_STRENGTH = os.getenv("WALLET_STRENGTH")
    PASSPHRASE_LENGHT = os.getenv("PASSPHRASE_LENGHT")
    KEYS_CONFIG_FILE = os.getenv("KEYS_CONFIG_FILE")