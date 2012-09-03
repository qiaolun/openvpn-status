# -*- coding: utf-8 -*-

from default_settings import *

try:
    from local_settings import *
    print 'Using local_settings'
except ImportError:
    print 'Using default_settings'
    pass

