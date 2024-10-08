from .base import *

from datetime import timedelta
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=45),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
}

DEBUG = True

ADMIN_EMAIL = config("ADMIN_EMAIL",default="admin@admin.com")
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_USE_TLS = False
EMAIL_HOST = config("EMAIL_HOST",default="smtp4dev")
EMAIL_HOST_USER = config("EMAIL_HOST_USER",default="")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD",default="")
EMAIL_PORT = 25



LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}
