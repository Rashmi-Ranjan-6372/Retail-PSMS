from pathlib import Path
from datetime import timedelta

# ---------------- BASE ---------------- #
BASE_DIR = Path(__file__).resolve().parent.parent


# ---------------- SECURITY ---------------- #
SECRET_KEY = 'django-insecure-v^ro0*w%s0hgz^xy(^jcw4bz$%bd$1+id5ckow8&=g+_&ba1z^'

DEBUG = True

ALLOWED_HOSTS = ['*']


# ---------------- APPLICATIONS ---------------- #
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party
    'rest_framework',

    # Local apps
    'accounts',
    # 'medicine',
    # 'inventory',
    # 'billing',
    # 'supplier',
]


# ---------------- MIDDLEWARE ---------------- #
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# ---------------- URLS ---------------- #
ROOT_URLCONF = 'config.urls'


# ---------------- TEMPLATES ---------------- #
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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


# ---------------- WSGI ---------------- #
WSGI_APPLICATION = 'config.wsgi.application'


# ---------------- DATABASE ---------------- #
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# ---------------- AUTH USER ---------------- #
AUTH_USER_MODEL = 'accounts.User'


# ---------------- PASSWORD VALIDATION ---------------- #
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


# ---------------- INTERNATIONALIZATION ---------------- #
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_TZ = True


# ---------------- STATIC FILES ---------------- #
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'


# ---------------- DEFAULT PK ---------------- #
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# ---------------- DRF CONFIG ---------------- #
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'accounts.authentication.CustomJWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}


# ---------------- JWT CONFIG ---------------- #
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=1),
    'AUTH_HEADER_TYPES': ('Bearer',),
}