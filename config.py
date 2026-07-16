import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY         = os.getenv('SECRET_KEY', 'fallback-secret-key')
    SUPABASE_URL       = os.getenv('SUPABASE_URL')
    SUPABASE_KEY       = os.getenv('SUPABASE_KEY')
    GEMINI_API_KEY     = os.getenv('GEMINI_API_KEY')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}