import os

dev = os.environ.get('DJANGO_DEV')
print dev
if dev:
	print 'dev'
	from .development import *
else:
	print 'heroku'
	from .heroku import *

