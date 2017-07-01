"""
Main class to interact with the phone and perform actions.
It has to implement  processMsg method that should return message
to be sent back to the GUI
"""

from pg import pgactions

class MsgHandler:
    def __init__(self, clientAndroid, ps):
        self.clientAndroid = clientAndroid
        self.ps = ps
        
        
    def setClientAndroid(self, clientAndroid):
        self.clientAndroid = clientAndroid

    def processMsg(self, tokens):
        print "MsgHandler.processMsg: Started pokestop handling"
        pgactions.look_around(self.clientAndroid, self.ps)
        print "MsgHandler.processMsg: Finished pokestop handling"
        
    

        
        