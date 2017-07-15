"""
This is a container class that has to hold all phone specific settings"
    touch_coordinates
    event_srcripts
    image_templates
"""

class PhoneSettings:
    def __init__(self, coords, scripts, templates):
        self.coords = coords
        self.scripts = scripts
        self.templates = templates
        self.skipPokemons = False
        self.clearBagCount = 10
        self.sectorsCount = 8
        self.isMaster = True
        self.slave = None
        
        #this is context variable
        self.dots_collection = dict()
    
    def getCoord(self, name):
        return self.coords[name]
    
    def getScript(self, name):
        return self.scripts[name]
    
    def getTemplate(self, name):
        return self.templates[name]
    
