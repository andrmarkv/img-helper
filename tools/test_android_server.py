import sys
import os

lib_path = os.path.abspath(os.path.join('..', 'pg'))
sys.path.append(lib_path)

from pg import serverAndroid

server = serverAndroid.ServerAndroid('localhost', 8003)
server.run()
