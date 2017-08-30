# Ask server.py whether we are on production or development server. Initialize appropriate settings modules accordingly.
from ._servers import get_server_type

exec("from .%s import *" % get_server_type())
