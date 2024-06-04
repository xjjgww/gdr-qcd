import os
import sys


sys.path.insert(0, os.path.dirname(__file__))

from myplant import create_app
application = create_app()
