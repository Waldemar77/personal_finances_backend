"""
Django settings for pft_backend project.

Generated by 'django-admin startproject' using Django 4.2.11.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
#import dj_database_url
import os
os.environ['LD_LIBRARY_PATH'] = '/usr/lib64'

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", default="your secret key")

# SECURITY WARNING: don't run with debug turned on in production!
# uncomment when we are deploying
DEBUG = "RENDER" not in os.environ

# comment this line when we are deploying
#DEBUG = True

# comment this line when we are deploying
#ALLOWED_HOSTS = ["*"]

# uncomment when we are deploying on Render
ALLOWED_HOSTS = []
RENDER_EXTERNAL_HOSTNAME = os.getenv("RENDER_EXTERNAL_HOSTNAME")
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)


# Application definition

DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

THIRD_APPS = [
    "rest_framework",
    "corsheaders",
    "dj_database_url",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

LOCAL_APSS = ["login.apps.LoginConfig"]

# We concatenate the list with the apps
INSTALLED_APPS = DJANGO_APPS + THIRD_APPS + LOCAL_APSS

CORS_ORIGIN_ALLOW_ALL = True

ROOT_URLCONF = "pft_backend.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "pft_backend.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    # >>> default database to interact with Render platform, we must use this one to deploy
    #"default": dj_database_url.config(
    #    default=f"postgres://{os.getenv('DB_USER', default='db_user')}:{os.getenv('DB_PASSWORD', default='db_pwd')}@{os.getenv('DB_HOST', default='db_host')}/{os.getenv('DB_NAME', default='db_name')}",
    #    conn_max_age=600,
    #)
    # ----> Connection with Azure SQL Database
    'default': {
        'ENGINE': 'mssql',
        'NAME': 'pft_database',  # Replace with your database name
        'USER': 'pft_db_admin',  # Replace with your database user
        'PASSWORD': 'Cicinho-369',  # Replace with your database password
        'HOST': 'pft-server.database.windows.net',  # Replace with your server name
        'PORT': '1433',  # Default port for SQL Server
        'OPTIONS': {
            'driver': 'ODBC Driver 17 for SQL Server'  # ODBC Driver 17
        }
    }

    # >>> to test in shell, we use this default database, external connection with postgresql
    #"default": dj_database_url.config(
    #    default=f"postgres://{os.getenv('DB_USER', default='db_user')}:{os.getenv('DB_PASSWORD', default='db_pwd')}@{os.getenv('DB_HOST', default='db_host')}.oregon-postgres.render.com/{os.getenv('DB_NAME', default='db_name')}",
    #    conn_max_age=600,
    #)

    # >>> to test in shell, we use this default database, external connection with postgresql
    #"default": dj_database_url.config(
    #    default=f"postgres://pftadmin:KeGrsweeS0qmWLZMNekkMnX6lhcoa3TG@dpg-cokp6q0l5elc73de8910-a.oregon-postgres.render.com/pft_database",
    #    conn_max_age=600,
    #)
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
USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

# This setting tells Django at which URL static files are going to be served to the user.
# Here, they well be accessible at your-domain.onrender.com/static/...
STATIC_URL = "/static/"

# Following settings only make sense on production and may break development environments.
if not DEBUG:  # Tell Django to copy statics to the `staticfiles` directory
    # in your application directory on Render.
    STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
    # Turn on WhiteNoise storage backend that takes care of compressing static files
    # and creating unique names for each version so they can safely be cached forever.
    STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
