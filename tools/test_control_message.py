import socket
import sys

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = ('localhost', 8002)

message = "%s;%d;%d" % ('TEST_ANDROID', 9999, 1)

try:

    # Send data
    print >>sys.stderr, 'sending "%s"' % message
    sent = sock.sendto(message, server_address)

finally:
    print >>sys.stderr, 'closing socket'
    sock.close()