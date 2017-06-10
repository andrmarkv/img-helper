import socket
import sys
import struct
from time import sleep
sys.path.append('../')
from pg import pgutil


def get_events_from_file(file_name):
    buf = ''
    f = open(file_name, 'r')
    lcount = 0
    
    
    for line in f:
        if len(line) <= 3:
            continue
        tokens = line.split(' ')

        if len(tokens) != 3:
            print "Got wrong line: " + line
            continue
        
        lcount = lcount + 1
                    
        for t in tokens:
            v = int(t.rstrip(), 16)
            u32 = v % 2**32
            buf = buf + struct.pack("<I", u32)
    
    f.close()
    
    print('lcount: %d, bufLen: %d') % (lcount, len(buf))
    
    return buf

if (len(sys.argv) < 3):
    print "Wrong arguments, should be: server_IP events_file"
    sys.exit(1) 

addr = sys.argv[1]

msg = get_events_from_file(sys.argv[2])

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = (addr, 8003)
print >>sys.stderr, 'connecting to %s port %s' % server_address
sock.connect(server_address)

try:
    
    # Send data
    msgid = 12345
    type = 4
    
    print >>sys.stderr, 'sending %d, %d, %s' % (msgid, type, "Touch event")
    v1 = struct.pack("<I", msgid)
    v2 = struct.pack("<I", type)
    buf = v1 + v2 + msg
    
    
    print >>sys.stderr, 'Message out'
    #pgutil.hexdump(buf)
    
    
    sock.sendall(struct.pack("<I", len(buf)))
    sock.sendall(buf)
    print >>sys.stderr, 'message len: %d was sent' % (len(buf))
    
    tmp = sock.recv(4)
    if tmp:
        data_len = struct.unpack("<I", tmp)[0]
        print 'received length: ' + str(data_len)
        data = sock.recv(data_len, socket.MSG_WAITALL)
        pgutil.hexdump(data)
        
    else:
        print 'Can not read reply'

finally:
    print >>sys.stderr, 'closing socket'
    sock.close()