import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

INSTANCE_DIR = os.path.join(BASE_DIR, "instance")
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads", "products")

os.makedirs(INSTANCE_DIR, exist_ok=True)
os.makedirs(UPLOAD_DIR, exist_ok=True)


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "temporary-development-key")

    SQLALCHEMY_DATABASE_URI = (
        "sqlite:///" + os.path.join(INSTANCE_DIR, "smart_shop.db")
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    UPLOAD_FOLDER = UPLOAD_DIR
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024