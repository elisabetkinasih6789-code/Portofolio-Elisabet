import os
from dotenv import load_dotenv
import mysql.connector
import cloudinary
import resend

# Membaca file .env dengan paksa dan MENGHAPUS ingatan lama (override=True)
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(BASE_DIR, '.env'), override=True)

SECRET_KEY = os.getenv("SECRET_KEY", "rahasia_untuk_session")

def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
            port=int(os.getenv("DB_PORT", 4000)),
            ssl_ca=os.getenv("DB_SSL_CA"),
            ssl_verify_cert=True
        )
        return connection, None
    except Exception as err:
        # Menampilkan sedikit bocoran password di browser untuk memastikan file .env terbaca benar
        bocoran_password = str(os.getenv("DB_PASSWORD"))[:3] + "***" 
        pesan_error = f"{str(err)} <br><br> (Info Debug: Password yang dicoba berawalan: {bocoran_password})"
        return None, pesan_error

if os.getenv("CLOUDINARY_CLOUD_NAME"):
    cloudinary.config(
        cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
        api_key=os.getenv("CLOUDINARY_API_KEY"),
        api_secret=os.getenv("CLOUDINARY_API_SECRET"),
        secure=True
    )

if os.getenv("RESEND_API_KEY"):
    resend.api_key = os.getenv("RESEND_API_KEY")