from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'auth_system',
        'USER': 'postgres',
        'PASSWORD': '[YOUR DATABASE PASSWORD]',
        'HOST': 'localhost'
    }
}
