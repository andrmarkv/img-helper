"""
Main class to handle communication with Android device and force it to do actions (capture screen, sendkeys). 
It allows sending message over the TCP socket and waits for response
Structure of the return message:
len(int), msgid(int), type(int), msg.
Handler is called based on the type of the message
"""
import socket
import struct
from time import sleep

import StringIO
from PIL import Image
import numpy as np

from pg import pgconst, pgutil

class ClientAndroid:
    def __init__(self, ip, port):
        self.server_address = (ip, port)

        # Create a UDP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        print 'ServerAndroid: starting up on %s port %s' % self.server_address
        
        self.sock.connect(self.server_address)
        
        #Set timeout for blocking read
        self.sock.settimeout(pgconst.ANDROID_CLIENT_RECV_TIMEOUT)
        
        self.msgId = 0;
        
    """
    Send message to the Android and wait for the response.
    Waiting is blocking for up to timeout seconds - timeout is defined in init method.
    As result it should return (type, data) of the response.
    In case of error it returns (None, None)
    """
    def sendMessage(self, mtype, msg):
        if self.sock is None:
            print "Error, can't send message - no connected client"
            return
        
        #increment message counter
        self.msgId = self.msgId + 1
        
        v1 = struct.pack("<I", self.msgId)
        v2 = struct.pack("<I", mtype)
        
        if (msg != None):
            buf = v1 + v2 + msg
        else:
            buf = v1 + v2
            
        self.sock.sendall(struct.pack("<I", len(buf)))
        self.sock.sendall(buf)
        
        #Wait for response and return type and data
        (t, data) = self.getResponse(self.msgId)

        return (t, data)
    
    """
    Wait for the response blocking for up to timeout seconds.
    As result it should return (type, data) of the response.
    In case of error it returns (None, None)
    """    
    def getResponse(self, reqMsgId):
        tmp = None
        try:
            #We need to receive 12 initial bytes 
            tmp = ''
            while len(tmp) < 12:
                b = self.sock.recv(12 - len(tmp), socket.MSG_WAITALL)
                tmp = tmp + b
        except socket.timeout, e:
            print 'Error! recv timed out, e:' + str(e)
        
        print 'received msg header:'
        pgutil.hexdump(tmp)    
        
        if tmp:
            data_len = struct.unpack_from("<I", tmp, 0)[0]
            print 'received length: ' + str(data_len)
            msgId = struct.unpack_from("<I", tmp, 4)[0]
            print 'received msgId: ' + str(msgId)
            t = struct.unpack_from("<I", tmp, 8)[0]
            print 'received type: ' + str(t)
            
            buf_size = data_len - 8
            data = ''
            while len(data) < buf_size:
                b = self.sock.recv(buf_size - len(data), socket.MSG_WAITALL)
                data = data + b
            print 'received bytes: ' + str(len(data))
                
            if (reqMsgId != msgId):
                print 'ERROR! got wrong msgId in response %d/%d' % (reqMsgId, msgId)    
            
            return (t, data)
        
        else:
            print 'Can not read reply'
            return (None, None)
        
    """
    execute screen capture and return it
    as numpy array of bytes (grey two dimentional, suitable for cv2 operations)
    Array is equal to cv2.imread('file.png', 0)
    """
    def get_screen_as_array(self):
        (t, data) = self.sendMessage(pgconst.MESSAGE_ANDROID_SCREEN_CAP, None)
        
        if (t != None and t == pgconst.MESSAGE_ANDROID_SCREEN_CAP):
            io = StringIO.StringIO(data)
            im = Image.open(io)
    
            if im is not None:
                a = np.array(im.convert('L'))
                
                print "Get Screen OK!"
                
                return a
    
        return None
        
        
    """
    Send touch to the Android device
    """
    def send_touch(self, (x, y), sleep_after=1):
        #pack coordinates into the message
        xb = struct.pack("<I", x)
        yb = struct.pack("<I", y)
        buf = xb + yb
        
        (t, data) = self.sendMessage(pgconst.MESSAGE_ANDROID_SEND_TOUCH, buf)
        
        if (t != None and t == pgconst.MESSAGE_ANDROID_SEND_TOUCH):
            print "Send touch: " + str(data)
            if sleep_after > 0:
                sleep(sleep_after)
            return 1;
    
        return None

    """
    Send swipe events to the Android device
    """
    def send_swipe(self, buf):
        (t, data) = self.sendMessage(pgconst.MESSAGE_ANDROID_SEND_SWIPE, buf)
        
        if (t != None and type == pgconst.MESSAGE_ANDROID_SEND_SWIPE):
            print "Send swipe: " + str(data)
            return 1;
    
        return None
    
    