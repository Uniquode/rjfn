# -*- coding: utf-8 -*-
# WSGI config for rjf project
import os
from utils import env
from django.core.wsgi import get_wsgi_application


env.load()
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rjf.settings")
application = get_wsgi_application()
