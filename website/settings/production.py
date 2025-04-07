from .base import *

DEBUG = False

ALLOWED_HOSTS = [
    'localhost',
    '206.189.112.151',
]

try:
    from .local import *
except ImportError:
    pass
