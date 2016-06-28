import sys, os
from application.settings import *

sys.path.append(os.path.join(BASE_DIR, 'feedcrunch/tests'))

from test_post_model import *
