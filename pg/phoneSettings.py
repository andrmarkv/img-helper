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
