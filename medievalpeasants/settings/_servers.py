# Script to determine hostname of current machine and send to __init__ to import appropriate settings.

from socket import gethostname

def get_server_type():
    server = gethostname()
    # Staircase is the hostname for Dreamhost, which is the vps provider I used for this project.
    if server == 'staircase':
        server = 'production'
    else:
        server = 'development'

    return server
