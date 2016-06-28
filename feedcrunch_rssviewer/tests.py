import sys, os
from application.settings import *

sys.path.append(os.path.join(BASE_DIR, 'feedcrunch_rssviewer/tests'))

from test_feedcrunch_rssviewer import *
