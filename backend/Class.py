# -*- coding: utf-8 -*-
"""
Created on Thu Apr 21 00:42:50 2022

@author: helen
"""
from Function import Function
from Parameter import Parameter
import sys
import io
import inspect
from parse_help_string import parse_class_text
from FlashcardElement import FlashcardElement

class Class(FlashcardElement):
    def __init__(self,clss):
        super().__init__(clss.__name__, clss.__module__)
        self.package_element = clss
        self.help_string = ""
        #TODO auch builtins? 
        class_callables = [getattr(clss,func) for func in dir(clss) if callable(getattr(clss, func)) and not func.startswith("__")]
        class_builtins = [b[1] for b in inspect.getmembers(clss,inspect.isbuiltin)]
        class_functions = class_callables+class_builtins
        class_functions = [fun for fun in class_functions if hasattr(fun,'__module__')]
        #if callable(getattr(clss, func)) and not func.startswith("__")]
        self.functions = [Function(f) for f in class_functions]
        #TODO only gets one constructor
        constructor = getattr(clss,'__init__')
        if hasattr(constructor, '__module__'):
            self.constructors = [Function(constructor)]
        else:
            self.constructors = []
        
    def toJSON(self):
        jsn = super().to_json()
        jsn['functions'] = [f.toJSON() for f in self.functions]
        jsn['constructors'] = [c.toJSON() for c in self.constructors]
        jsn['full_name'] = self.full_name
        return jsn
    
    def set_help_strings(self, stringBuffer):
        stringBuffer = io.StringIO()
        sys.stdout = stringBuffer
        help(self.package_element)
        self.help_string = stringBuffer.getvalue()
        for f in self.functions:
            f.set_help_strings(stringBuffer)
        for c in self.constructors:
            c.set_help_strings(stringBuffer)
            
    def set_descriptions(self):
        if  self.help_string:
            try:
                jsn = parse_class_text(self.help_string,self.name)
            except:
                jsn = {}
            if 'description' in jsn.keys():
                self.description = jsn['description']
            func_names = [func.name for func in self.functions]
            if 'functions' in jsn.keys():
                for extracted_func in  jsn['functions']:
                    try:
                        idx = func_names.index(extracted_func['name'])
                        self.functions[idx].set_descriptions(extracted_func)                 
                    except ValueError:
                        pass
            if 'constructors' in jsn.keys():
                for extracted_const in jsn['constructors']:
                    if 'description' in extracted_const.keys():
                        if self.constructors:
                            self.constructors[0].description = extracted_const['description']
                        
                    
            