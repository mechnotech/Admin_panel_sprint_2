from .base import *

DATABASES = {
    'default': {
        'ENGINE': os.environ.get('DB_ENGINE'),
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('POSTGRES_USER'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': 5432,
        'CONN_MAX_AGE': 60,
        'OPTIONS': {
            'options': '-c search_path=public,content'
        }
    }
}

INSTALLED_APPS += [
    'debug_toolbar',
    'django_extensions',
]
MIDDLEWARE.append('debug_toolbar.middleware.DebugToolbarMiddleware')
INTERNAL_IPS = ['127.0.0.1', ]

