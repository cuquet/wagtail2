import random
import string

import dj_database_url

from .base import *

DEBUG = True
# DJANGO_SECRET_KEY *should* be specified in the environment. If it's not, generate an ephemeral key.
if 'DJANGO_SECRET_KEY' in os.environ:
    SECRET_KEY = os.environ['DJANGO_SECRET_KEY']
else:
    # Use if/else rather than a default value to avoid calculating this if we don't need it
    print("WARNING: DJANGO_SECRET_KEY not found in os.environ. Generating ephemeral SECRET_KEY.")
    SECRET_KEY = ''.join([random.SystemRandom().choice(string.printable) for i in range(50)])

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# BASE_URL required for notification emails
BASE_URL = 'http://localhost:8000'

db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)

# Simplified static file serving.
# https://warehouse.python.org/project/whitenoise/

MIDDLEWARE.append('whitenoise.middleware.WhiteNoiseMiddleware')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

RECAPTCHA_PUBLIC_KEY = os.environ['RECAPTCHA_PUBLIC_KEY']
RECAPTCHA_PRIVATE_KEY = os.environ['RECAPTCHA_PRIVATE_KEY']

RECAPTCHA_DISABLE = True
# COMPRESS_ENABLED = True
# LIBSASS_SOURCE_COMMENTS = True

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}
