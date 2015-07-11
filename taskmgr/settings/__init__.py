import os
 
dev = os.environ.get('DJANGO_DEV')
print dev
if dev:
    from .development import *
else:
    from .heroku import *

