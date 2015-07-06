from os import environ

if environ.get('HEROKU_ENV') is not None:
	from .herokusettings import *
else:
	from .base import *