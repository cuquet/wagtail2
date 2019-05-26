import random
import string

from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# DJANGO_SECRET_KEY *should* be specified in the environment. If it's not, generate an ephemeral key.
if 'DJANGO_SECRET_KEY' in os.environ:
    SECRET_KEY = os.environ['DJANGO_SECRET_KEY']
else:
    # Use if/else rather than a default value to avoid calculating this if we don't need it
    print("WARNING: DJANGO_SECRET_KEY not found in os.environ. Generating ephemeral SECRET_KEY.")
    SECRET_KEY = ''.join([random.SystemRandom().choice(string.printable) for i in range(50)])

# Make sure Django can detect a secure connection properly on Heroku:
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Redirect all requests to HTTPS
SECURE_SSL_REDIRECT = os.getenv('DJANGO_SECURE_SSL_REDIRECT', 'off') == 'on'

# If True, the SecurityMiddleware sets the X-Content-Type-Options: nosniff header
# on all responses that do not already have it.
# SECURE_CONTENT_TYPE_NOSNIFF = True

# If True, the SecurityMiddleware sets the X-XSS-Protection: 1; mode=block header
# on all responses that do not already have it.
# SECURE_BROWSER_XSS_FILTER = True

# If the header is set to DENY then the browser will block the resource from loading
#  in a frame no matter which site made the request
# X_FRAME_OPTIONS = 'DENY'

# the cookie will be marked as “secure,” which means browsers may ensure that the cookie is
# only sent under an HTTPS connection.
# SESSION_COOKIE_SECURE = True

# the cookie will be marked as “secure,” which means browsers may ensure that the cookie is
# only sent with an HTTPS connection.
# CSRF_COOKIE_SECURE = True

# Accept all hostnames, since we don't know in advance which hostname will be used for any given Heroku instance.
# IMPORTANT: Set this to a real hostname when using this in production!
# See https://docs.djangoproject.com/en/1.10/ref/settings/#allowed-hosts
ALLOWED_HOSTS = [env.list('DJANGO_ALLOWED_HOSTS', '*')]

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# BASE_URL required for notification emails
BASE_URL = 'http://localhost:8000'

DATABASES = {
    'default': env.db('DATABASE_URL_PROD', default='sqlite:////tmp/wagtaildb'),
}

# configure CACHES from CACHE_URL environment variable (defaults to locmem if no CACHE_URL is set)
CACHES = {
    # read os.environ['CACHE_URL'] and raises ImproperlyConfigured exception if not found
    'default': env.cache(),
    # read os.environ['REDIS_URL']
    # 'redis': env.cache('REDIS_URL')
}

# Simplified static file serving.
# http://whitenoise.evans.io/en/stable/django.html
MIDDLEWARE.append('whitenoise.middleware.WhiteNoiseMiddleware')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

RECAPTCHA_PUBLIC_KEY = env('RECAPTCHA_PUBLIC_KEY')
RECAPTCHA_PRIVATE_KEY = env('RECAPTCHA_PRIVATE_KEY')
RECAPTCHA_DISABLE = False

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
            'level': env('DJANGO_LOG_LEVEL', 'INFO'),
        },
    },
}
