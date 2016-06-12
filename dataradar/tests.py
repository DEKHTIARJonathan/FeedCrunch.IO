import sys, os
from application.settings import *

sys.path.append(os.path.join(BASE_DIR, 'dataradar/tests'))

from test_dataradar_models import *
