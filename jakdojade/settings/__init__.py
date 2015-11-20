SECRET_KEY = ''
CLIENT_KEY = ''

try:
    from .settings import CLIENT_KEY, SECRET_KEY
except ImportError as e:
    pass
