"""
Django settings for gmail2sfdc project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import django.conf.global_settings as DEFAULT_SETTINGS
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

env = os.environ['GMAIL2SFDC_ENV'] if 'GMAIL2SFDC_ENV' in os.environ else None

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '8l4$=lvq$s)0vsym7wlbcjw4f3))nxhuna&j4ytdg$z%xc9!!+'

# SECURITY WARNING: don't run with debug turned on in production!
if env == 'local':
    DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = '*'


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sessions',
    'south',
    'accounts',
    'gmail2sfdc',
    'zaps'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'gmail2sfdc.urls'

WSGI_APPLICATION = 'gmail2sfdc.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'gmail2sfdcdb',
        'USER': 'eltropy',
        'PASSWORD': 'swhad0o9',
        'HOST': '127.0.0.1',
        'PORT': '5432',
        }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = "/home/ubuntu/gmail2sfdc/static/"

#custom settings

TEMPLATE_CONTEXT_PROCESSORS = DEFAULT_SETTINGS.TEMPLATE_CONTEXT_PROCESSORS + (
    'django.core.context_processors.request',
)

if env == 'local':
    GOOGLE_CLIENT_ID = '9655458160-942191vjqk0kl6fkdtmalqnfpece691v.apps.googleusercontent.com'

    GOOGLE_CLIENT_SECRET = 'XWJR57YKU7Ro3zenItPcQ6z6'

    GOOGLE_REDIRECT_URI = 'http://localhost:8000/auth/googleAuthCallback'

    SFDC_CLIENT_ID = '3MVG9A2kN3Bn17htG_Lafomxe8JS2zgynZ84.Yjm3WU0f2SFvMc9LcjzJExWzHTsTvvLxuq_j8a8ZXPGTBEPq'

    SFDC_CLIENT_SECRET = '1110308827261502813'

    SFDC_REDIRECT_URI = 'http://localhost:8000/auth/sfdcAuthCallback'
else:
    GOOGLE_CLIENT_ID = '9655458160-hp9apvkhskbjrha00h4qo0l7kje0isep.apps.googleusercontent.com'

    GOOGLE_CLIENT_SECRET = 'AXjCcaejnrzs8ZVZgVVaVcll'

    GOOGLE_REDIRECT_URI = 'http://gmail2sfdc.tk/auth/googleAuthCallback'

    SFDC_CLIENT_ID = '3MVG9A2kN3Bn17htG_Lafomxe8Ee3W.bdZUHb3XVsUqx2hD2OMMuEUZ0DN_34Oe8IfYbfM5BEcT9bsNtebRlR'

    SFDC_CLIENT_SECRET = '8643476575507910945'

    SFDC_REDIRECT_URI = 'https://gmail2sfdc.tk/auth/sfdcAuthCallback'


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format' : "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt' : "%d/%b/%Y %H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
        },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'gmail2sfdc.log',
            'formatter': 'verbose'
        },
        },
    'loggers': {
        'django': {
            'handlers':['file'],
            'propagate': True,
            'level':'DEBUG',
            },
        'gmail2sfdc': {
            'handlers': ['file'],
            'level': 'DEBUG',
            },
        }
}