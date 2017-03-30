#!/bin/python

import socket
import subprocess

import pgutil

msgId = 0;

class ControlServer:
    def __init__(self, ip, port):
        self.server_address = (ip, port)

        # Create a UDP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        print 'ControlServer: starting up on %s port %s' % self.server_address
        self.sock.bind(self.server_address)
    
    def test(self):
        print "ControlServer.test: self.server_address:" + str(self.server_address)
        
        
    def run(self):
        while True:
            global msgId;
            print '\nControlServer.run: waiting for a message'
            data, address = self.sock.recvfrom(4096)
            
            print 'ControlServer.run: received %s bytes from %s' % (len(data), address)
            print data
            
            if data and len(data) > 10:
                tokens = data.split(';')
        
                if len(tokens) < 2:
                    print "ControlServer.run: Error! got wrong message: " + data
                    continue
                
                command = tokens[0]
                
                if command == 'CONTROL':
                    a = pgutil.get_screen_as_array()
                    
                    if a is None:
                        print "ControlServer.run: Error! Can't capture the screen."
                    
                    print "ControlServer.run: Started pokestop"
                    subprocess.call(['/usr/bin/adb', 'shell', 'sh', '/sdcard/Download/mi5_check.stop.sh'])
                    print "ControlServer.run: Finished pokestop"
                    #time.sleep(10);
                    msgId = msgId + 1;
                    msg = "%s;%d;%d" % ('CONTROL', msgId, 1)
                    sent = self.sock.sendto(msg, address)
                    print 'ControlServer.run: sent %s bytes back to %s' % (sent, address)
