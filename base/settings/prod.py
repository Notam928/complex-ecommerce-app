from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["julesecommerceapp.herokuapp.com"]

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases
import dj_database_url
db_from_env = dj_database_url.config(conn_max_age=500)


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

DATABASES['default'].update(db_from_env)
