#!/bin/python

import socket
import subprocess

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the port
server_address = ('localhost', 8002)
print 'starting up on %s port %s' % server_address
sock.bind(server_address)

msgId = 0;

while True:
    global msgId;
    print '\nwaiting for a message'
    data, address = sock.recvfrom(4096)
    
    print 'received %s bytes from %s' % (len(data), address)
    print data
    
    if data and len(data) > 10:
        tokens = data.split(';')

        if len(tokens) < 2:
            print "Error! got wrong message: " + data
            continue
        
        
        print "Started pokestop"
        subprocess.call(['/usr/bin/adb', 'shell', 'sh', '/sdcard/Download/mi5_check.stop.sh'])
        print "Finished pokestop"
        #time.sleep(10);
        msgId = msgId + 1;
        msg = "%s;%d;%d" % ('CONTROL', msgId, 1)
        sent = sock.sendto(msg, address)
        print 'sent %s bytes back to %s' % (sent, address)
