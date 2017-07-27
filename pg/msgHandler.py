"""
Main class to interact with the phone and perform actions.
It has to implement  processMsg method that should return message
to be sent back to the GUI
"""

import socket

from pg import pgactions
from pg import pgconst

class MsgHandler:
    def __init__(self, clientAndroid, ps):
        self.clientAndroid = clientAndroid
        self.ps = ps
        self.msgCount = 0
        
        self.sock = None
        if (self.ps.isMaster and self.ps.slave is not None):
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        
    def setClientAndroid(self, clientAndroid):
        self.clientAndroid = clientAndroid

    def processMsg(self, tokens):
        self.msgCount = self.msgCount + 1
        
        #Forward message to slave nodes if we have one
        if(self.sock is not None):
            message = ""
            for t in tokens:
                message = message + t + ";"
                
            self.sock.sendto(message, self.ps.slave)
             
        print "MsgHandler.processMsg: Started pokestop handling"
        
        if self.msgCount % self.ps.clearBagCount == 0:
            self.perform_clear_bag()
        
        pgactions.look_around(self.clientAndroid, self.ps)
        print "MsgHandler.processMsg: Finished pokestop handling"
        
    def perform_clear_bag(self):
        print "MsgHandler.processMsg: Started clearing bag"
        #items = pgconst.DEL_ITEMS_NANAB_BERRY | pgconst.DEL_ITEMS_POTION | pgconst.DEL_ITEMS_RAZZ_BERRY | pgconst.DEL_ITEMS_REVIVE
        items = pgconst.DEL_ITEMS_NANAB_BERRY | pgconst.DEL_ITEMS_POTION | pgconst.DEL_ITEMS_RAZZ_BERRY
        pgactions.clear_bag(self.clientAndroid, items, self.ps)
    

        
        