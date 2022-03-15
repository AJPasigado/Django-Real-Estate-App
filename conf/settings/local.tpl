DEBUG = True
ALLOWED_HOSTS = ['*']

DATABASES = {
    # Ends with "postgresql", "mysql", "sqlite3" or "oracle".
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'db_name',
        'USER': 'db_user',
        'PASSWORD': 'db_password',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    },
}

INSTALLED_APPS += ["django_extensions"]
