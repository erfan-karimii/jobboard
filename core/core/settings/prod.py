from .base import *
from decouple import config


DEBUG = False
CSRF_TRUSTED_ORIGINS = config(
    "CSRF_TRUSTED_ORIGINS",
    cast=lambda v: [s.strip() for s in v.split(",")],
    default="http://*",
)

ADMIN_EMAIL = config("ADMIN_EMAIL",default="admin@admin.com")
EMAIL_BACKEND = "django.core.mail.backends.dummy.EmailBackend"
EMAIL_USE_TLS = False
EMAIL_HOST = config("EMAIL_HOST",default="smtp4dev")
EMAIL_HOST_USER = config("EMAIL_HOST_USER",default="")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD",default="")
EMAIL_PORT = 25