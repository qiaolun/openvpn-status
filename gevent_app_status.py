#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gevent.wsgi import WSGIServer
from app_status import app, settings

http_server = WSGIServer((settings.LISTEN_HOST, settings.LISTEN_PORT), app)
http_server.serve_forever()
