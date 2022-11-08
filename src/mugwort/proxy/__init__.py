# -*- coding: utf-8 -*-

try:
    import requests
    import yaml
    import apscheduler
except ImportError:
    print('Module [mugwort.proxy.clash] not imported, execute `pip install apscheduler requests pyyaml` will import it')
else:
    from .clash import ClashProxy, ClashConfig
