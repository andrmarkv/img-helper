"""
Main class to interact with the phone and perform actions.
It has to implement  processMsg method that should return message
to be sent back to the GUI
"""

from pg import pgutil
from pg import pgconst

import subprocess
import time

class MsgHandler:
    def __init__(self, templates):
        self.templates = templates

    def processMsg(self, tokens):
        img = pgutil.get_screen_as_array()
                    
        if img is None:
            print "MsgHandler.processMsg: Error! Can't capture the screen."
        
        print "MsgHandler.processMsg: Started pokestop handling"
        
        if pgutil.is_main_map(img, self.templates)[0]:
            self.send_pokestop_touch_events()
        elif pgutil.is_menu(img, self.templates)[0]:
            self.send_close_menu_touch_events()
            time.sleep(1)
            self.send_pokestop_touch_events()
        else:
            self.send_close_menu_touch_events()
        
        print "MsgHandler.processMsg: Finished pokestop handling"
        
        
    def send_pokestop_touch_events(self):
        script = self.templates[pgconst.TEMPLATE_INSIDE_POKESTOP][3]
        subprocess.call(['/usr/bin/adb', 'shell', 'sh', script])
        
    def send_close_menu_touch_events(self):
        script = self.templates[pgconst.TEMPLATE_MENU][4]
        subprocess.call(['/usr/bin/adb', 'shell', 'sh', script])
        
        