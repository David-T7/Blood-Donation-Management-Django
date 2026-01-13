import os
from dotenv import load_dotenv

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# Load the .env file
load_dotenv(os.path.join(BASE_DIR, '.env'))

# Pull the SECRET_KEY from the environment
SECRET_KEY = os.getenv('SECRET_KEY')

# Convert the string 'True' from .env into a Python Boolean
DEBUG = os.getenv('DEBUG') == 'True'
ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'UserAccount',
    'widget_tweaks',
    'axes',
    'django_google_maps',
    'Donor',
    'Blood',
    'Hospital',
    'Event',
    'BBManager',
    'Nurse',
    'LabTechnician',
]

LOCATION_FIELD = {
    'map.provider': 'google',
    'search.provider': 'google',
    'provider.google.api': '//maps.google.com/maps/api/js?sensor=false',
    'provider.google.api_key': 'AIzaSyDHWvCvLbnxDhrYnpp0UBLE4PZ0na8fRRQ',
    'provider.google.api_libraries': '',
    'provider.google.map.type': 'ROADMAP',
}



AUTH_USER_MODEL = 'UserAccount.Account'
#LOGOUT_REDIRECT_URL = 'home'
AUTHENTICATION_BACKENDS = [
# AxesBackend should be the first backend in the AUTHENTICATION_
'axes.backends.AxesBackend',
# Django ModelBackend is the default authentication backend.
'django.contrib.auth.backends.ModelBackend',
]



MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'axes.middleware.AxesMiddleware',
]




SILENCED_SYSTEM_CHECKS = ['axes.W003']
AXES_ONLY_ADMIN_SITE = False
AXES_ONLY_USER_FAILURES = True
AXES_COOLOFF_TIME = 2
ROOT_URLCONF = 'BloodBankManagement.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates')
        ],
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
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]


WSGI_APPLICATION = 'BloodBankManagement.wsgi.application'
DEFAULT_AUTO_FIELD='django.db.models.AutoField' 

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'blood_bank',
#         'USER': 'root',
#         'PASSWORD': '1234',
#         'HOST': '127.0.0.1',
#         'PORT': '3306',
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

# AUTH_PASSWORD_VALIDATORS = [
#     {
#         'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
#     },
# ]


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

MEDIA_URL = '/images/'
STATIC_URL = '/static/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'static/images')





