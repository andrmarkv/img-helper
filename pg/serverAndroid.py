"""
Main class to handle communication with ANdroid device and force it to do actions (capture screen, sendkeys). 
It allows sending message over the TCP socket and calls handler for different return message types
Structure of the return message:
len(int), msgid(int), type(int), msg.
Handler is called based on the type of the message
"""
import socket
import struct

import pgutil
from multiprocessing import Queue
from pg import pgconst

msgId = 0;

class ServerAndroid:
    def __init__(self, ip, port):
        self.server_address = (ip, port)

        # Create a UDP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        print 'ServerAndroid: starting up on %s port %s' % self.server_address
        self.sock.bind(self.server_address)

        self.sock.listen(0)
        
        self.conn = None #member bield to represent current connection
        
        self.queue = Queue()
    
    def handleMessage(self, data):
        global msgId;
        
        msgId = msgId + 1;
        
        pgutil.hexdump(data)
        
        id = struct.unpack("<I", data[0:4])[0]
        type = struct.unpack("<I", data[4:8])[0]
        msg = data[8:]

        print "Got message id: %d, type: %d, msglen: %d" % (id, type, len(msg))

        if type == pgconst.MESSAGE_ANDROID_TYPE_TEST:
            self.sendMessageNoWait(id, pgconst.MESSAGE_ANDROID_TYPE_TEST, "OK!")
        else:
            self.queue.put((id, type, msg))
        
        
    def run(self):
        while True:
            connection, client_address = self.sock.accept()
            self.conn = connection #create 
            
            try:
                print 'ServerAndroid.run: got connection: ' + str(client_address)
                while True:
                    tmp = connection.recv(4)
                    if tmp:
                        data_len = struct.unpack("<I", tmp)[0]
                        print 'ServerAndroid.run: received length: ' + str(data_len)
                        data = connection.recv(data_len)
                        print 'ServerAndroid.run: received bytes: ' + str(data_len)
                        
                        self.handleMessage(data)
                    else:
                        print 'ServerAndroid.run: closed connection: ' + str(client_address)
                        break
            finally:
                connection.close()
                
        print 'ServerAndroid.run: exit'
        
    def sendMessage(self, msgId, type, msg, timeout):
        if self.conn is None:
            print "Error, can't send message - no connected client"
            return
        
        v1 = struct.pack("<I", msgId)
        v2 = struct.pack("<I", type)
        buf = v1 + v2 + msg
        self.conn.sendall(struct.pack("<I", len(buf)))
        self.conn.sendall(buf)
        
#         (id, type, msg) = self.queue.get(timeout)
#         if id == msgId:
#             print msg
#         else:
#             print "Got wrong message, was expecting id: %d, received: %d" % (msgId, id)

        return (type, msg)
    
    def sendMessageNoWait(self, msgId, type, msg):
        if self.conn is None:
            print "Error, can't send message - no connected client"
            return
        
        v1 = struct.pack("<I", msgId)
        v2 = struct.pack("<I", type)
        buf = v1 + v2 + msg
        self.conn.sendall(struct.pack("<I", len(buf)))
        self.conn.sendall(buf)

        return
    
    
    