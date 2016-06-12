import sys, os
from application.settings import *

sys.path.append(os.path.join(BASE_DIR, 'dataradar_webviewer/tests'))

from test_dataradar_webviewer import *
