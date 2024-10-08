"""
Django settings for news_portal project.

Generated by 'django-admin startproject' using Django 4.2.13.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
import os
from pathlib import Path

config_file = 'C:/Users/Admin/Desktop/config.txt'
with open(config_file, 'r') as f:
    info_list = [line.strip() for line in f]


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-i_-@(o-+pa)%ke32)7*5#m6ywpyn_h&b1dw!l0hzbcev#8ogv$'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []
# ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    'django.contrib.sites',
    'django.contrib.flatpages',
    
    'mymodel',
    
    'accounts',
    
    'allauth',
    'allauth.account',
    
    # Необязательно — требуется установка с использованием `django-allauth[socialaccount]`.
    'allauth.socialaccount',
    
    # ... включите провайдеров, которых вы хотите включить:
    'allauth.socialaccount.providers.yandex',
    
    'subscriptions',
    'django_apscheduler',
]

# Запуск скриптов django_apscheduler автоматически
SCHEDULER_AUTOSTART = True

SITE_ID = 1
STATICFILES_DIRS = [BASE_DIR / 'static']

LOGIN_REDIRECT_URL = '/news'
LOGOUT_REDIRECT_URL = '/news'

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = True
ACCOUNT_UNIQUE_USERNAME = True
ACCOUNT_AUTHENTICATION_METHOD = 'username'
ACCOUNT_EMAIL_VERIFICATION = 'none'


EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
DEFAULT_FROM_EMAIL = 'admin@example.com'


# --------------------- НАСТРОЙКИ CELERY ---------------------
# ------------------------------------------------------------
# Если вы используете Redis Labs, то переменные CELERY_BROKER_URL и CELERY_RESULT_BACKEND должны строиться по шаблону:
# redis://логин:пароль@endpoint:port

# info_list = [Public endpoint URL, Public endpoint PORT, Security Default user password]

CELERY_BROKER_URL = f'redis://default:{info_list[2]}@{info_list[0]}:{info_list[1]}'  # Указывает на URL брокера сообщений (Redis). По умолчанию он находится на порту 6379
CELERY_RESULT_BACKEND = f'redis://default:{info_list[2]}@{info_list[0]}:{info_list[1]}'  # Указывает на хранилище результатов выполнения задач
CELERY_ACCEPT_CONTENT = ['application/json']  # Допустимый формат данных
CELERY_TASK_SERIALIZER = 'json'  # Метод сериализации задач
CELERY_RESULT_SERIALIZER = 'json'  # Метод сериализации результатов

# Также обратите внимание, что Celery с версией выше 4+ не поддерживается Windows.
# Поэтому если у вас версия Python 3.10 и выше,
# запускайте Celery, добавив в команду флаг: --pool=solo.

# Для запуска Celery нужно быть в директории project

# Запустить Celery:
# celery -A proj_name worker -l INFO
# celery -A proj_name worker -l INFO --pool=solo

# Для запуска периодических задач на Windows запустите в разных окнах терминала:
# celery -A proj_name worker -l INFO --pool=solo
# celery -A proj_name beat -l INFO
# ------------------------------------------------------------


# ------------------ НАСТРОЙКИ КЭШИРОВАНИЯ -------------------
# ------------------------------------------------------------
# Кэширование через файловую систему
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': os.path.join(BASE_DIR, 'cache_files'),  # Указываем, куда будем сохранять кэшируемые файлы! Не забываем создать папку cache_files внутри папки с manage.py!
        'TIMEOUT': 60*5,  # По умолчанию кэш обновляется каждые 300 сек
    }
}

# Были замечены проблемы при использовании БД кэша и базы данных SQlite,
# поэтому будьте осторожны при их совместном использовании!
# Тем не менее при использовании других СУБД неполадок замечено не было.
# ------------------------------------------------------------


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',

    # Add the account middleware:
    "allauth.account.middleware.AccountMiddleware",
]

ROOT_URLCONF = 'news_portal.urls'

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

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    
    # Define formatters
    'formatters': {
        'console_verbose': {
            'format': '%(asctime)s %(levelname)s %(message)s',
        },
        'console_warning': {
            'format': '%(asctime)s %(levelname)s [%(pathname)s] %(message)s',
        },
        'console_error': {
            'format': '%(asctime)s %(levelname)s [%(pathname)s] %(message)s',
            'exc_info': True,
        },
        'file_general': {
            'format': '%(asctime)s %(levelname)s [%(module)s] %(message)s',
        },
        'file_error': {
            'format': '%(asctime)s %(levelname)s [%(pathname)s] %(message)s',
            'exc_info': True,
        },
        'file_security': {
            'format': '%(asctime)s %(levelname)s [%(module)s] %(message)s',
        },
    },
    
    # Define filters
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
    },
    
    # Define handlers
    'handlers': {
        'console_debug': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'console_verbose',
        },
        'console_warning': {
            'level': 'WARNING',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'console_warning',
        },
        'console_error': {
            'level': 'ERROR',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'console_error',
        },
        'file_general': {
            'level': 'INFO',
            'filters': ['require_debug_false'],
            'class': 'logging.FileHandler',
            'filename': 'general.log',
            'formatter': 'file_general',
        },
        'file_errors': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': 'errors.log',
            'formatter': 'file_error',
        },
        'file_security': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'filename': 'security.log',
            'formatter': 'file_security',
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
            'formatter': 'file_error',  # Use the same format as in errors.log but without exc_info
            'include_html': True,
        },
    },
    
    # Define loggers
    'loggers': {
        'django': {
            'handlers': ['console_debug', 'console_warning', 'console_error', 'file_general'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'django.request': {
            'handlers': ['file_errors', 'mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.server': {
            'handlers': ['file_errors', 'mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.template': {
            'handlers': ['file_errors'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.db.backends': {
            'handlers': ['file_errors'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.security': {
            'handlers': ['file_security'],
            'level': 'WARNING',
            'propagate': False,
        },
    }
}


WSGI_APPLICATION = 'news_portal.wsgi.application'


AUTHENTICATION_BACKENDS = [
    # Needed to log in by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by email
    'allauth.account.auth_backends.AuthenticationBackend',
]

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

# USE_TZ = True
USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
