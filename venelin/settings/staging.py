import os
from .production import *  # NOQA

DEBUG = os.getenv("DEBUG") in ("true", "True", "1")
