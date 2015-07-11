import os
 
dev = os.environ.get('DJANGO_DEV', 'YES')
 
if dev:
    from .development import *
else:
    from .heroku import *

