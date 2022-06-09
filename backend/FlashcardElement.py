# -*- coding: utf-8 -*-
"""
Created on Thu Apr 21 19:43:39 2022

@author: helen
"""

class FlashcardElement:
    #name, description, full name, module name
    def __init__(self,name,module_name):
        self.name = name
        self.module_name = module_name
        self.description = ""
        self.full_name = f"{self.module_name}.{self.name}"
        
    def to_json(self):
        jsn = {"name":self.name,
               "module_name":self.module_name, 
               "description":self.description,
               "full_name": self.full_name}
        return jsn