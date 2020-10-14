# -*- coding: utf-8 -*-
# ASGI config for rjf project
import os
from django.core.asgi import get_asgi_application
from utils import env


env.load()
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rjf.settings")
application = get_asgi_application()
