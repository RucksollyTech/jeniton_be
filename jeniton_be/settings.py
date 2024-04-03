
from pathlib import Path
import os
from decouple import config
from dj_database_url import parse as dburl
from datetime import timedelta
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config("DEBUG", default=False, cast=bool)
ALLOWED_HOSTS_FOR_DEV = ["*"]
ALLOWED_HOSTS_FOR_PRODUCTION = []

ALLOWED_HOSTS = ALLOWED_HOSTS_FOR_DEV if DEBUG else ALLOWED_HOSTS_FOR_PRODUCTION



# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # jeniton
    'jeniton.apps.JenitonConfig',
    'corsheaders',
    'storages',
    'rest_framework',
    "django_extensions",
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'jeniton_be.urls'

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

WSGI_APPLICATION = 'jeniton_be.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

dev_dburl = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

ma_default = 'sqlite:///' + os.path.join(BASE_DIR, 'db.sqlite3')
# DATABASES_DEV = {'defaults': dj_database_url.config(default=dev_dburl)}
DATABASES_PRO = {'default': dj_database_url.config(default=ma_default)}
# DATABASES = DATABASES_DEV if DEBUG else DATABASES_PRO
DATABASES = DATABASES_PRO

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'

STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')



# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'




CORS_FOR_DEV = [
    "http://localhost:3000",
    "http://localhost:8000",
    "http://localhost"
]

CORS_FOR_PRODUCTION = [
    "https://www.kidsmulticulturalworld.org"
]

CORS_ALLOWED_ORIGINS = CORS_FOR_DEV if DEBUG else CORS_FOR_PRODUCTION

DEFAULT_RENDERER_CLASSES = [
    'rest_framework.renderers.JSONRenderer',
]

DEFAULT_AUTHENTICATION_CLASSES = [
    # 'rest_framework_simplejwt.authentication.JWTAuthentication',
    'rest_framework.authentication.TokenAuthentication',
]
if DEBUG:
    DEFAULT_RENDERER_CLASSES += [
        'rest_framework.renderers.BrowsableAPIRenderer',
    ]
REST_FRAMEWORK = {
    
    'DEFAULT_AUTHENTICATION_CLASSES': DEFAULT_AUTHENTICATION_CLASSES,
    'DEFAULT_RENDERER_CLASSES': DEFAULT_RENDERER_CLASSES,
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
        'rest_framework.parsers.JSONParser',
     )
}


CLIENT_ID = config("CLIENT_ID")
CLIENT_SECRETE = config("CLIENT_SECRETE")

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# env('EMAIL_HOST')
EMAIL_HOST = config("EMAIL_HOST")
EMAIL_HOST_USER = config("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD")
EMAIL_PORT = 465
EMAIL_USE_TLS = False
EMAIL_USE_SSL = True

FRONTEND_URL = config("FRONTEND_URL")
ADMIN_EMAIL_ADDRESSS= "kryspatra.services@gmail.com"

AWS_ACCESS_KEY_ID=config("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY=config("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME=config("AWS_STORAGE_BUCKET_NAME")


AWS_QUERYSTRING_AUTH = False

# to prevent overiding pictures with same
# name on the server

AWS_S3_FILE_OVERWRITE = False

AWS_DEFAULT_ACL = None
if not DEBUG: 
    DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"

