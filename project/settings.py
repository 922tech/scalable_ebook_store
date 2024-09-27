import os
import sys
from datetime import timedelta
from pathlib import Path

import redis


MODE_TESTING = sys.argv[1:2] == ['test']

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "this_is_secret!!")

DEBUG = os.getenv("DJANGO_DEBUG", False) == "True"

ALLOWED_HOSTS = os.getenv("DJANGO_ALLOWED_HOSTS", '*').split(",")

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_simplejwt.token_blacklist',
    'corsheaders',
    'django_filters',
    'django_otp',
    'apps.users',
    'apps.store',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django_otp.middleware.OTPMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'project.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('POSTGRES_DB', 'project'),
        'USER': os.getenv('POSTGRES_USER', 'postgres'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD', 'postgres'),
        'HOST': os.getenv('POSTGRES_HOST', 'postgres'),
        'PORT': int(os.getenv('POSTGRES_PORT', '5432')),
    },
    'search': {
        'backend': 'plugins.typesense_adapter.typesense.TypesenseBackend',
        'config': {
            'nodes': [
                {
                    'host': os.getenv('TYPESENSE_HOST', 'localhost'),
                    'port': os.getenv('TYPESENSE_PORT', '8108'),
                    'protocol': os.getenv('TYPESENSE_PROTOCOL', 'http')
                }
            ],
            'api_key': os.getenv('TYPESENSE_API_KEY', 'xyz'),
            'connection_timeout_seconds': int(os.getenv('TYPESENSE_CONNECTION_TIMEOUT_SECONDS', 2))
        }
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': os.getenv('REDIS_ADDRESS', 'redis://127.0.0.1:6379/1'),
        'OPTIONS': {
            # If your Redis instance requires a password
            'PASSWORD': os.getenv('REDIS_PASSWORD', ''),
            # Connection timeout in seconds
            'SOCKET_CONNECT_TIMEOUT': os.getenv('SOCKET_CONNECT_TIMEOUT', 5),
            # Operation timeout in seconds
            'SOCKET_TIMEOUT': os.getenv('SOCKET_TIMEOUT', 5),
        }
    }
}
AUTHENTICATION_BACKENDS = [
    'django_otp.backends.OTPBackend',
    'django.contrib.auth.backends.ModelBackend',
]
AUTH_USER_MODEL = 'users.User'
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en'

TIME_ZONE = os.getenv('TIME_ZONE', 'Asia/Tehran')

USE_I18N = True

USE_L10N = True

USE_TZ = True

LANGUAGES = [
    ('en', 'English'),
    ('fa', 'Persian')
]

LOCALE_PATHS = [os.path.join(BASE_DIR, 'locale')]

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, "static")

# Media files
MEDIA_URL = 'media/'
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# Cors
CORS_ORIGIN_ALLOW_ALL = bool(os.getenv('CORS_ORIGIN_ALLOW_ALL', 1))
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_WHITELIST = [
    "http://localhost:3000",
]

SECURE_REFERRER_POLICY = 'same-origin'
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

################################################################################################
#                                    3rd-Parties
################################################################################################
REDIS = redis.Redis(host=os.getenv('REDIS_HOST', 'redis'),
                    password=os.getenv('REDIS_PASSWORD'))

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissions'
    ],
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'project.throttles.RouteBasedUserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '300/second' if MODE_TESTING else '10/second',
        'user': '300/second' if MODE_TESTING else '10/second',
    },
    'DEFAULT_PAGINATION_CLASS': 'project.pagination.LimitedLimitOffsetPagination',
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(minutes=120),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
    'ALGORITHM': 'RS256',
    'SIGNING_KEY': SECRET_KEY,
}

# LOGGER SETTINGS
DJANGO_FLUENTD_SERVER = os.getenv('FLUENTD_HOST', '')
DJANGO_FLUENTD_PORT = 24224
DJANGO_FLUENTD_TAG = "app"
REQUEST_LOGGING_ENABLE_COLORIZE = False
os.makedirs(f'{str(BASE_DIR)}/logs', exist_ok=True)

CLOUD_STORAGE_CLIENT_CONFIG = {
    'backend': 'plugins.minio_adapter.minio_adapter.MinioAdapter',
    'bucket_name': os.getenv('MINIO_PUBLIC_BUCKET_NAME', 'public'),
    'config': {
        'endpoint': os.getenv('MINIO_ENDPOINT_URL', 'localhost:9000'),
        'access_key': os.getenv('MINIO_ACCESS_KEY', 'BUCKET_ACCESS_KEY'),
        'secret_key': os.getenv('MINIO_SECRET_KEY', 'BUCKET_SECRET_KEY'),
        'secure': bool(os.getenv('BUCKET_SECURE', 0)),
    }
}

CELERY_BROKER_URL = os.getenv(
    "CELERY_BROKER_URL", default='redis://redis:6379/0')
CELERY_RESULT_BACKEND = os.getenv(
    "CELERY_RESULT_BACKEND", default='redis://redis:6379/0')
CELERY_ACCEPT_CONTENT = ['application/json', 'application/x-python-serialize']
CELERY_TASK_SERIALIZER = 'pickle'
CELERY_RESULT_SERIALIZER = 'pickle'
CELERY_TIMEZONE = TIME_ZONE

FILE_UPLOAD_CHECK_DELAY = 1200
