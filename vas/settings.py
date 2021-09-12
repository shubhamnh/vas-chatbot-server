import os
import environ
from datetime import timedelta

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.str('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool('DEBUG', default=False)

ALLOWED_HOSTS = env.str('ALLOWED_HOSTS').split(',')

AUTH_USER_MODEL = 'users.User'

# Application definition

INSTALLED_APPS = [
    # Django Apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third Party Apps
	'rest_framework',
    'rest_framework.authtoken',
	'corsheaders',
    'push_notifications',

    # Local
    'users.apps.UsersConfig',
    'academics.apps.AcademicsConfig',
    'chatbot.apps.ChatbotConfig',
    'api.apps.ApiConfig',
]

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=600),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
}

# Django Push Notification Settings
# See https://github.com/jazzband/django-push-notifications

PUSH_NOTIFICATIONS_SETTINGS = {
        # "FCM_API_KEY": "[your api key]",
        # "GCM_API_KEY": "[your api key]",
        # "APNS_CERTIFICATE": "/path/to/your/certificate.pem",
        # "APNS_TOPIC": "com.example.push_test",
        # "WNS_PACKAGE_SECURITY_ID": "[your package security id, e.g: 'ms-app://e-3-4-6234...']",
        # "WNS_SECRET_KEY": "[your app secret key, e.g.: 'KDiejnLKDUWodsjmewuSZkk']",
        "WP_PRIVATE_KEY": env.str('WP_PRIVATE_KEY'),
        "WP_CLAIMS": {'sub': "mailto: "+env.str('WP_CLAIMS_EMAIL')}
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
	'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CORS_ORIGIN_WHITELIST = env.str('CORS_ORIGIN_WHITELIST').split(',')

ROOT_URLCONF = 'vas.urls'

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

WSGI_APPLICATION = 'vas.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': env.db('DATABASE_URL')
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': os.path.join(BASE_DIR, 'vas.sqlite3'),
    # }
}

RASA_URL = env.str('RASA_URL')

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.MD5PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
    'django.contrib.auth.hashers.BCryptPasswordHasher',
    'django.contrib.auth.hashers.SHA1PasswordHasher',
    'django.contrib.auth.hashers.UnsaltedSHA1PasswordHasher',
    'django.contrib.auth.hashers.UnsaltedMD5PasswordHasher',
    'django.contrib.auth.hashers.CryptPasswordHasher',
]

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
