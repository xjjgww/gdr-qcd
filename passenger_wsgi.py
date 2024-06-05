import os
import sys


sys.path.insert(0, os.path.dirname(__file__))

from mygdr import create_app
application = create_app()
