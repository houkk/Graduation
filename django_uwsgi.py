import os

os.environ['PYTHON_EGG_CACHE'] = '/<a path>/.python-eggs'
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "GraduationProject.settings")
# from django.core.wsgi import get_wsgi_application
# application = get_wsgi_application()
from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
