"""
Main class to handle communication with app.js application and process
Control requests. It receives message on the UDP socket and calls handle
method of the MsgHandler class. Server address and MsgHandler is devined duriing
initialization of the instance.
serverAndroid is running instance of the phone controlling server
"""
import socket

import pgutil

msgId = 0;

class ServerControl:
    def __init__(self, ip, port, handler, serverAndroid):
        self.server_address = (ip, port)

        # Create a UDP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        print 'ControlServer: starting up on %s port %s' % self.server_address
        self.sock.bind(self.server_address)
        
        self.serverAndroid = serverAndroid
        
        self.handler = handler
        self.handler.setServerAndroid(serverAndroid)
    
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
                    self.handler.processMsg(tokens)
                    msgId = msgId + 1;
                    msg = "%s;%d;%d" % ('CONTROL', msgId, 1)
                    sent = self.sock.sendto(msg, address)
                    print 'ControlServer.run: sent %s bytes back to %s' % (sent, address)
                    
