import sys
import os
sys.path.append("./certifaiReferenceModelServer")
from certifaiReferenceModelServer.utils.local_server import assemble_server

def start_all():
    path=os.path.abspath(__file__)
    fp = os.path.join(os.path.dirname(path),'.s2i/environment')
    with open(fp,'r') as fn:
        routes=fn.read().replace("ROUTES=", '')
        assemble_server(routes)


if __name__ == '__main__':
    start_all()