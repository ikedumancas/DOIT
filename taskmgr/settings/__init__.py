import os

dev = os.environ.get('DJANGO_DEV')
if dev:
	from .development import *
else:
	from .heroku import *

