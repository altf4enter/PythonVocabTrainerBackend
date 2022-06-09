# -*- coding: utf-8 -*-
"""
Created on Thu Apr 21 00:21:05 2022

@author: helen
"""
from Parameter import Parameter
import inspect
import sys
import io
from parse_help_string import parse_function_text
from FlashcardElement import FlashcardElement

class Function(FlashcardElement):
    def __init__(self, func):
        super().__init__(func.__name__,func.__module__)
        self.package_element = func
        self.help_string = ""
        try: 
            self.parameters = [Parameter(param) for param in list(inspect.signature(func).parameters.values()) ]
        except ValueError:
            self.parameters = []
        
    
    def toJSON(self):
        jsn = super().to_json()
        jsn['parameters'] = [param.toJSON() for param in self.parameters]
        jsn['description']= self.description
        jsn['full_name'] = self.full_name
        return jsn
    
    def set_help_strings(self, stringBuffer):
        stringBuffer = io.StringIO()
        sys.stdout = stringBuffer
        help(self.package_element)
        self.help_string = stringBuffer.getvalue()
        
    def set_descriptions(self,jsn=None):
        if  self.help_string:
            if jsn is None:
                try:
                    jsn = parse_function_text(self.help_string,self.name)
                except:
                    jsn = {}
            if 'description' in jsn.keys():
                self.description = jsn['description']
            func_param_names = [param.name for param in self.parameters]
            if 'parameters' in jsn.keys():
                for extracted_param in  jsn['parameters']:
                    try:
                        idx = func_param_names.index(extracted_param['name'])
                        if 'description' in extracted_param.keys():
                            self.parameters[idx].set_description(extracted_param['description'])                 
                    except ValueError:
                        pass
                    