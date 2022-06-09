# -*- coding: utf-8 -*-
"""
Created on Thu Apr 21 00:07:35 2022

@author: helen
"""
import inspect
from FlashcardElement import FlashcardElement

class Parameter(FlashcardElement):
    def __init__(self, inspect_parameter):
        super().__init__(inspect_parameter.name, "")
        if inspect_parameter.default != inspect.Parameter.empty:
            default = ""
            if hasattr(inspect_parameter.default,'__name__'):
                self.default_value = inspect_parameter.default.__name__
            else:
                self.default_value = str(inspect_parameter.default)
        
    def set_description(self, description):
        self.description = description
    
    def toJSON(self):
        jsn = super().to_json()
        if hasattr(self, 'default_value'):
            jsn['default'] = self.default_value
        return jsn
    
    
            