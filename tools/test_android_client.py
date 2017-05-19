import socket
import sys
import struct

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('localhost', 8003)
print >>sys.stderr, 'connecting to %s port %s' % server_address
sock.connect(server_address)

try:
    
    # Send data
    msgid = 12345
    type = 999
    message = 'This is the message.  It will be repeated.'
    print >>sys.stderr, 'sending %d, %d, %s' % (msgid, type, message)
    v1 = struct.pack("<I", msgid)
    v2 = struct.pack("<I", type)
    buf = v1 + v2 + message
    sock.sendall(struct.pack("<I", len(buf)))
    sock.sendall(buf)

finally:
    print >>sys.stderr, 'closing socket'
    sock.close()