"""
Django settings for saketime_project project.

Generated by 'django-admin startproject' using Django 2.2.12.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os, environ, cloudinary

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)

env.read_env('.env')

# DEBUG = env('DEBUG')
# REDIS_URL = env('REDIS_URL')
#
# CHANNEL_LAYERS = {
#     "default": {
#         "BACKEND": "channels_redis.core.RedisChannelLayer",
#         "CONFIG": {"hosts": [REDIS_URL]},
# } }

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# EMAIL_CONFIG = env.email_url('EMAIL_URL')
# vars().update(EMAIL_CONFIG)
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['warm-anchorage-76492.herokuapp.com', '127.0.0.1']

# Application definition

INSTALLED_APPS = [
    "whitenoise.runserver_nostatic",
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'main.apps.MainConfig',
    'django_tables2',
    'users.apps.UsersConfig',
    'rest_framework',
    'cloudinary',

]




cloudinary.config(
    cloud_name = env('cloud_name'),
    api_key = env('cloud_api_key'),
    api_secret = env('cloud_secret_key'),
    secure = True
)

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES':
        ('rest_framework.authentication.SessionAuthentication',
         'rest_framework.authentication.BasicAuthentication'),
    'DEFAULT_PERMISSION_CLASSES':
        ('rest_framework.permissions.DjangoModelPermissions',),
    'DEFAULT_FILTER_BACKENDS':
        ('django_filters.rest_framework.DjangoFilterBackend',),
    'DEFAULT_PAGINATION_CLASS':
        'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 100
}

DJANGO_TABLES2_TEMPLATE = 'django_tables2/bootstrap.html'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'main.middlewares.cart_middleware',
]

ROOT_URLCONF = 'saketime_project.urls'

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

WSGI_APPLICATION = 'saketime_project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'saketime_db',
        'USER': 'postgres',
        'PASSWORD': 'deadp00l',
        'HOST': 'localhost',
        'POST': '5432',


    }
}

# import dj_database_url
#
# db_from_env = dj_database_url.config(conn_max_age=600)
# DATABASES['default'].update(db_from_env)


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
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'


if not DEBUG:
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST_USER = "username"
    EMAIL_HOST = 'smtp.domain.com'
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True
    EMAIL_HOST_PASSWORD = "password"
else:
    EMAIL_BACKEND = (
        "django.core.mail.backends.console.EmailBackend"
    )

AUTH_USER_MODEL = 'users.User'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
LOGIN_URL = '/'
