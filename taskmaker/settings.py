import os
from pathlib import Path
from dotenv import load_dotenv
# Build paths inside the templates like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv()

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get("DEBUG")

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

CSRF_TRUSTED_ORIGINS=os.environ.get("CSRF_TRUSTED_ORIGINS", "").split()

# Application definition

INSTALLED_APPS = [
    "users.apps.UsersConfig",
    "projects.apps.ProjectsConfig",
    "widget_tweaks",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "admin_honeypot",
    "channels",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
]

ROOT_URLCONF = "taskmaker.urls"

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            # Standard directory for your templates's templates
            os.path.join(BASE_DIR, 'templates'),
        ],
        'APP_DIRS': True,  # Allows template loading from application directories
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


#WSGI_APPLICATION = "taskmaker.wsgi.application"
ASGI_APPLICATION="taskmaker.asgi.application"
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': "channels_redis.core.RedisChannelLayer",
        'CONFIG': {
            "hosts": [os.environ.get('REDIS_URL')],
        },
    },
}

AUTHENTICATION_BACKENDS = [
    'users.login_verification.EmailVerifiedBackend',
]


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': os.environ.get("DATABASE_ENGINE"),
        'NAME': os.environ.get("DATABASE_NAME"),
        'USER': os.environ.get("DATABASE_USER"),
        'PASSWORD': os.environ.get("DATABASE_PASSWORD"),
        "HOST":os.environ.get("DATABASE_HOST"),
        "PORT":os.environ.get("DATABASE_PORT"),
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

STATIC_URL = "static/"
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

EMAIL_BACKEND = os.environ.get("EMAIL_BACKEND")
EMAIL_HOST = os.environ.get("EMAIL_HOST")
EMAIL_PORT = os.environ.get("EMAIL_PORT")
EMAIL_USE_TLS = os.environ.get("EMAIL_USE_TLS")
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")

MAX_UPLOAD_SIZE=int(eval(os.environ.get("MAX_UPLOAD_SIZE")))

ACCOUNT_USERNAME_BLACKLIST=["admin", "profile", "employee"]

CELERY_BROKER_URL=os.environ.get("CELERY_BROKER_URL")
CELERY_RESULT_BACKEND=os.environ.get("CELERY_BROKER_URL")
CELERY_ACCEPT_CONTENT=["json"]
CELERY_TASK_SERIALIZER="json"
CELERY_RESULT_SERIALIZER = 'json'
