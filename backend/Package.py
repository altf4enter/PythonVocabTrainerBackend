# -*- coding: utf-8 -*-
"""
Created on Thu Apr 21 01:06:54 2022

@author: helen
"""

from Class import Class
from Function import Function
import inspect
import sys
import io

class Package():
    def __init__(self,package):
        print(package.__name__)
        self.name = package.__name__
        self.package_element = package
        #TODO does not get builtin functions
        self.functions = [Function(f) for f in self.getFunctions(package)]
        self.classes = [Class(c) for c in self.getClasses(package)]
        self.submodules = [Package(submodule) for submodule in self.getSubmodules(package)]
        
        
    def getFunctions(self,package):
        child_functions = inspect.getmembers(package, inspect.isfunction)
        child_builtins = inspect.getmembers(package,inspect.isbuiltin)
        child_functions = child_functions+child_builtins
        return [getattr(package,name) for name,tpe in child_functions if tpe.__module__ == package.__name__]
    
    def getClasses(self,package):
        child_classes = inspect.getmembers(package, inspect.isclass)
        return [getattr(package,name) for name,tpe in child_classes if tpe.__module__ == package.__name__]
        
    def getSubmodules(self,package):
        child_modules = inspect.getmembers(package, inspect.ismodule)
        submodules = []
        for module_name,tpe in child_modules:
            submodule = getattr(package, module_name)
            if submodule.__name__.startswith(package.__name__):
                submodules.append(submodule)
        return submodules
        
    def set_help_strings(self,stringBuffer=None):
        old_stdout = sys.stdout
        first = stringBuffer is None
        if first:
            stringBuffer = io.StringIO()
            sys.stdout = stringBuffer
        for f in self.functions:
            f.set_help_strings(stringBuffer)
        for c in self.classes:
            c.set_help_strings(stringBuffer)
        for s in self.submodules:
            s.set_help_strings(stringBuffer=stringBuffer)
        if first:
            sys.stdout = old_stdout
            
    def set_descriptions(self):
        for f in self.functions:
            f.set_descriptions()
        for c in self.classes:
            c.set_descriptions()
        for s in self.submodules:
            s.set_descriptions()
        
    def toJSON(self):
        jsn ={"name":self.name}
        jsn['functions'] = [fun.toJSON() for fun in self.functions]
        jsn['classes'] = [c.toJSON() for c in self.classes]
        jsn['packages'] = [p.toJSON() for p in self.submodules]
        return jsn