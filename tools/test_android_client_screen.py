import socket
import sys
import struct
from time import sleep
sys.path.append('../')
from pg import pgutil

if (len(sys.argv) < 2):
    print "Please specify server IP"
    sys.exit(1) 

addr = sys.argv[1]

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = (addr, 8003)
print >>sys.stderr, 'connecting to %s port %s' % server_address
sock.connect(server_address)

try:
    
    # Send data
    msgid = 12345
    type = 2
    print >>sys.stderr, 'sending %d, %d' % (msgid, type)
    v1 = struct.pack("<I", msgid)
    v2 = struct.pack("<I", type)
    buf = v1 + v2
    sock.sendall(struct.pack("<I", len(buf)))
    sock.sendall(buf)
    print >>sys.stderr, 'message len: %d was sent' % (len(buf))
    
    sleep(2);
    
    #We need to receive 12 initial bytes 
    tmp = ''
    while len(tmp) < 12:
        b = sock.recv(12 - len(tmp), socket.MSG_WAITALL)
        tmp = tmp + b

    pgutil.hexdump(tmp)
    
    if tmp:
        data_len = struct.unpack_from("<I", tmp, 0)[0]
        print 'received length: ' + str(data_len)
        msgId = struct.unpack_from("<I", tmp, 4)[0]
        print 'received msgId: ' + str(msgId)
        type = struct.unpack_from("<I", tmp, 8)[0]
        print 'received type: ' + str(type)
        
        buf_size = data_len - 8
        data = ''
        while len(data) < buf_size:
            b = sock.recv(buf_size - len(data), socket.MSG_WAITALL)
            data = data + b
        print 'received bytes: ' + str(len(data))
        
        newFile = open("/tmp/test.png", "wb")
        newFileByteArray = bytearray(data)
        newFile.write(newFileByteArray)
        newFile.flush()
        newFile.close()
        
    else:
        print 'Can not read reply'

finally:
    print >>sys.stderr, 'closing socket'
    sock.close()