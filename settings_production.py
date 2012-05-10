# Load settings first
try:
    from settings import *
except ImportError:
    pass

# Now override any of them
LOCAL = False
DEBUG = False
TEMPLATE_DEBUG = DEBUG


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'iellos',
        'USER': 'root',
        'PASSWORD': '!IE77os@',
        'HOST': '',
        'PORT': '',
    }
}
