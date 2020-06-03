"""
Django settings for harvester project.

Generated by 'django-admin startproject' using Django 2.2.10.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
import sys
from sentry_sdk.integrations.logging import ignore_logger

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# We're adding the environments directory outside of the project directory to the path
# That way we can load the environments and re-use them in different contexts
# Like maintenance tasks and harvesting tasks
sys.path.append(os.path.join(BASE_DIR, "..", "environments"))
from surfpol import environment, MODE, get_package_info
# Then we read some variables from the (build) environment
PACKAGE_INFO = get_package_info()
GIT_COMMIT = PACKAGE_INFO.get("commit", "unknown-git-commit")
VERSION = PACKAGE_INFO.get("versions").get("harvester", "0.0.0")

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = environment.secrets.django.secret_key

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = environment.django.debug

# We're disabling the ALLOWED_HOSTS check, because containers will run in a VPC environment
# This environment is expected to be unreachable with disallowed hosts.
# It hurts to have this setting enabled on AWS, because health checks don't pass the domain check.
ALLOWED_HOSTS = ["*"]

USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')


# Application definition

INSTALLED_APPS = [
    'harvester',  # first to override runserver command
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'core',
    'edurep',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'harvester.urls'

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

WSGI_APPLICATION = 'harvester.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'harvester',
        'USER': environment.django.postgres_user,
        'PASSWORD': environment.secrets.postgres.password,
        'HOST': environment.django.postgres_host,
        'PORT': 5432,
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, '..', 'static')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
WHITENOISE_ALLOW_ALL_ORIGINS = True


# Logging
# https://docs.djangoproject.com/en/2.2/topics/logging/
# https://docs.sentry.io/

if not DEBUG:
    # We kill all DisallowedHost logging on the servers,
    # because it happens so frequently that we can't do much about it
    ignore_logger('django.security.DisallowedHost')


# Elastic Search
# https://www.elastic.co/guide/index.html

ELASTICSEARCH_USER = environment.elastic_search.username
ELASTICSEARCH_PASSWORD = environment.secrets.elastic_search.password
ELASTICSEARCH_HOST = environment.elastic_search.host
ELASTICSEARCH_PROTOCOL = environment.elastic_search.protocol
ELASTICSEARCH_ANALYSERS = {
    'en': 'english',
    'nl': 'dutch'
}


# Project Open Leermaterialen

MIME_TYPE_TO_FILE_TYPE = {  # TODO: this is Edurep based, how do we want this for other repositories?
    'unknown': 'unknown',
    'application/pdf': 'pdf',
    'application/x-pdf': 'pdf',
    'application/vnd.openxmlformats-officedocument.presentationml.presentation': 'presentation',
    'application/vnd.openxmlformats-officedocument.presentationml.slideshow': 'presentation',
    'application/vnd.ms-powerpoint': 'presentation',
    'application/ppt': 'presentation',
    'application/msword': 'text',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document': 'text',
    'application/rtf': 'text',
    'text/plain': 'text',
    'text/html': 'text',
    'application/vnd.ms-word': 'text',
    'application/vnd.ms-word.document.macroEnabled.12': 'text',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.template': 'text',
    'text/rtf':	'text',
    'application/xhtml+xml': 'text',
    'application/postscript': 'text',
    'application/vnd.ms-publisher':	'text',
    'text/xml': 'text',
    'application/vnd.oasis.opendocument.spreadsheet': 'spreadsheet',
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': 'spreadsheet',
    'application/vnd.ms-excel': 'spreadsheet',
    'video/flv': 'video',
    'video/x-flv': 'video',
    'video/quicktime': 'video',
    'video': 'video',
    'video/x-msvideo': 'video',
    'video/mpeg': 'video',
    'application/x-mplayer2': 'video',
    'video/mp4': 'video',
    'video/x-ms-wmv': 'video',
    'video/x-ms-asf': 'video',
    'image': 'image',
    'image/bmp': 'image',
    'image/pjpeg': 'image',
    'image/png': 'image',
    'image/x-icon': 'image',
    'image/x-ms-bmp': 'image',
    'image/tiff': 'image',
    'image/jpg': 'image',
    'image/gif': 'image',
    'image/jpeg': 'image',
    'application/zip': 'archive',
    'application/x-tar': 'archive',
    'application/x-stuffit': 'archive',
    'application/x-rar-compressed': 'archive',
    'application/x-Wikiwijs-Arrangement': 'archive',
    'audio/mpeg': 'audio',
    'application/x-koan': 'audio',
    'application/vnd.koan':	'audio',
    'audio/midi': 'audio',
    'audio/x-wav': 'audio',
    'application/octet-stream': 'other',
    'application/x-yossymemo':	'digiboard',
    'application/Inspire': 'digiboard',
    'application/x-AS3PE': 'digiboard',
    'application/x-Inspire': 'digiboard',
    'application/x-smarttech-notebook': 'digiboard',
    'application/x-zip-compressed': 'digiboard',
    'application/x-ACTIVprimary3': 'digiboard',
    'application/x-ibooks+zip':	'ebook',
    'message/rfc822': 'message',
    'application/vnd.google-earth.kmz': 'googleearth',
    'application/x-java': 'app',
}

EXTENSION_TO_FILE_TYPE = {  # TODO: we should map from extension to mime and then file_type
    '.html': 'text',
    '.pdf': 'pdf',
    '.pptx': 'presentation',
    '.ppt': 'presentation',
    '.doc': 'text',
    '.docx': 'text',
    '.rtf': 'text',
    '.txt': 'text',
    '.xls': 'spreadsheet',
    '.xlsx': 'spreadsheet',
    '.png': 'image',
    '.jpeg': 'image',
    '.jpg': 'image',
    '.zip': 'zip',
}