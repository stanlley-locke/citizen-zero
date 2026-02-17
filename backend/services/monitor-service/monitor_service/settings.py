from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-monitor-service-key'
DEBUG = True
ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'apps.dashboard',
    'apps.config_manager',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'apps.monitoring.TrafficControlMiddleware',
]

ROOT_URLCONF = 'monitor_service.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'monitor_service.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = []
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True
STATIC_URL = 'static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CORS_ALLOW_ALL_ORIGINS = True

# Monitoring Config
MONITORED_SERVICES = [
    {"name": "auth-service", "url": "http://127.0.0.1:8000/api/v1/auth/monitor/metrics/", "ping": "http://127.0.0.1:8000/api/v1/auth/health/"},
    {"name": "id-service", "url": "http://127.0.0.1:8001/api/v1/monitor/metrics/", "ping": "http://127.0.0.1:8001/api/v1/health/"},
    {"name": "verify-service", "url": "http://127.0.0.1:8002/api/v1/verify/monitor/metrics/", "ping": "http://127.0.0.1:8002/api/v1/verify/health/"},
    {"name": "audit-service", "url": "http://127.0.0.1:8003/api/v1/audit/monitor/metrics/", "ping": "http://127.0.0.1:8003/api/v1/audit/health/"},
    {"name": "iprs-mock", "url": "http://127.0.0.1:8005/api/v1/monitor/metrics/", "ping": "http://127.0.0.1:8005/api/v1/citizens/"},
    {"name": "monitor-service", "url": "http://127.0.0.1:8006/api/v1/monitor/metrics/", "ping": "http://127.0.0.1:8006/api/v1/health/"},
]
