import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    DEBUG = os.getenv('DEBUG') == 'True'
    REDIS_URL = os.getenv('REDIS_URL')
    DATABASE_NAME = os.getenv('DATABASE_NAME')
    DATABASE_USER=os.getenv('DATABASE_USER')
    DATABASE_PASSWORD=os.getenv('DATABASE_PASSWORD')
    DATABASE_HOST=os.getenv('DATABASE_HOST')
    DATABASE_PORT=os.getenv('DATABASE_PORT')
    JWT_SECRET=os.getenv('JWT_SECRET')
    SMTP_FROM=os.getenv('SMTP_FROM')
    SMTP_PASSWORD=os.getenv('SMTP_PASSWORD')
    SMTP_HOST=os.getenv('SMTP_HOST')
    SMTP_PORT=os.getenv('SMTP_PORT')
    ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS').split(',')
    MINIO_URL = os.getenv('MINIO_URL')
    MINIO_ACCESS_KEY = os.getenv('MINIO_ACCESS_KEY')
    MINIO_SECRET_KEY = os.getenv('MINIO_SECRET_KEY')
    MINIO_BUCKET = os.getenv('MINIO_BUCKET')
    LLM_API_URL = os.getenv('LLM_API_URL')
    SCAN_BUCKET = os.getenv('SCAN_BUCKET')
    S3_REGION = os.getenv('S3_REGION')
    LLM_MODEL_NAME = os.getenv('LLM_MODEL_NAME')

