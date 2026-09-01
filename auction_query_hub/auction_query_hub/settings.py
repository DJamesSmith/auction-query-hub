import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")
SECRET_KEY = os.getenv("SECRET_KEY")
DEBUG = True
ALLOWED_HOSTS = ['127.0.0.1', '192.168.0.105']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',               # For APIs
    'users',                        # Users app
    'auctions',                     # auctions app
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'auction_query_hub.urls'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'auction_query_hub.wsgi.application'
DATABASES = {
    "default": {
        "ENGINE":   "django.db.backends.postgresql",
        "NAME":     os.getenv("DB_NAME"),
        "USER":     os.getenv("DB_USER"),
        "PASSWORD": os.getenv("DB_PASSWORD"),
        "HOST":     os.getenv("DB_HOST"),
        "PORT":     os.getenv("DB_PORT"),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    { 'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator' },
    { 'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator' },
    { 'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator' },
    { 'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator' },
]


LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / "static"]



# NOTE:
# CREATE DATABASE auction_query_hub_db OWNER django_user;

# analytics is not an app but a folder created manually.

# Add ['192.168.0.100'] to ALLOWED_HOSTS depending on the mac's IP address

# Run this command for running on localhost in flutter app (Means: Django, listen for connections coming through any network interface on port 8000):
# python manage.py runserver 0.0.0.0:8000

# how to find my Mac's IP ?
# ipconfig getifaddr en0
# 192.168.0.105
# This change is to be made in flutter app's baseurl, django's settings.py

# Bulk INSERT queries:
# INSERT INTO users (username, email, password, role, created_at) VALUES
# ('john', 'john@gmail.com', 'john123', 'Buyer', CURRENT_TIMESTAMP),
# ('rahul', 'rahul@gmail.com', 'rahul123', 'Seller', CURRENT_TIMESTAMP),
# ('priya', 'priya@gmail.com', 'priya123', 'Buyer', CURRENT_TIMESTAMP),
# ('admin', 'admin@gmail.com', 'admin123', 'Admin', CURRENT_TIMESTAMP),
# ('punam', 'punam@gmail.com', 'punam123', 'Seller', CURRENT_TIMESTAMP),
# ('jimmy', 'jimmy@gmail.com', 'jimmy123', 'Seller', CURRENT_TIMESTAMP);

# INSERT INTO auction_items (title, description, base_price, current_price, start_time, end_time, seller_id) VALUES
# ('Gaming Laptop', 'Intel i7, RTX 4060, 16GB RAM', 50000.00, 51000.00, '09:00:00', '18:00:00', 2),
# ('iPhone 15', '128GB, Excellent Condition', 60000.00, 62000.00, '10:00:00', '20:00:00', 2),
# ('DJI Drone', '4K Camera Drone', 35000.00, 37000.00, '08:30:00', '16:30:00', 2),
# ('PlayStation 5', 'PS5 Disc Edition', 40000.00, 42000.00, '12:00:00', '21:00:00', 2),
# ('MacBook Pro', 'M1 Pro, 16GB RAM, 256GB SSD', 80000.00, 82000.00, '11:00:00', '19:00:00', 6);
