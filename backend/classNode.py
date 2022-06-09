# -*- coding: utf-8 -*-
"""
Created on Tue Apr 12 12:23:48 2022

@author: helen
"""

import re
import uuid
from anytree import Node, RenderTree
from functionDescriptionNode import FunctionDescriptionNode
from clean_data import clean_description

class ClassNode(Node):
  pythonic_char = r"[A-Za-z0-9\_]"

  def __init__(self,text,classname, parent=None, children=None, **kwargs):
      #here, get name as label
      if not self.isClassDescription(text,classname):
        raise Exception(f"{text} does not contain a class definition")
      self.text = text
      self.classname = classname
      name = uuid.uuid4()
      super().__init__(name,parent=parent,children=children,**kwargs)

  def toJSON(self):
      class_dict = {"name": self.classname}
      
      defs = [node.text for node in self.children if type(node) == Node]
      class_dict["description"] = clean_description(" ".join(defs))

      func_nodes = [node for node in self.children if type(node) == FunctionDescriptionNode]
      #TODO das sind jetzt class functions
      constructors = [node for node in func_nodes if node.func_name == self.classname]
      self_const = FunctionDescriptionNode(re.sub("^class\s+","",self.text))
      self_const.children = self.children
      constructors.append(self_const)
      class_dict["constructors"] = [node.toJSON() for node in constructors]

      funcs = [node for node in func_nodes if node.func_name != self.classname]
      class_dict["functions"] = [node.toJSON() for node in funcs]
      return class_dict
      

  @staticmethod
  def isClassDescription(text,classname=None):
    #function_regex = rf"{classname}\s*\((\s*{parameter_init}\s*,?)+\)"
      text = re.sub("^class\s+","",text) 
      if FunctionDescriptionNode.isFunctionDescription(text):
        node = FunctionDescriptionNode(text)
        if node.func_name == classname:
          return True
      return False