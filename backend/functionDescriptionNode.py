# -*- coding: utf-8 -*-
"""
Created on Tue Apr 12 12:21:24 2022

@author: helen
"""

import re
import uuid
from anytree import Node, RenderTree
from parameterNode import ParameterNode
from clean_data import clean_description


class FunctionDescriptionNode(Node):
  pythonic_char = r"[A-Za-z0-9\_/\*<>]"
  #TODO (a,a,a,a,a,...) als funktionsparameter
  #TODO <> als optionale werteparameter
  #TODO kann auch **irgendwas heißen
  parameter_init = rf"(\s*|{pythonic_char}+|\(\s*({pythonic_char}+\s*,?)\)|\[\s*{pythonic_char}+\s*\]|{pythonic_char}+\s*=\s*[^,]+|(\*args)|(\*\*kwargs)|/|\.+)"
  function_regex = rf"{pythonic_char}+\s*\((\s*{parameter_init}\s*,?)+\)"

  def __init__(self,text, parent=None, children=None, **kwargs):
      #here, get name as label
      if not self.isFunctionDescription(text):
        raise Exception(f"{text} does not contain a function definition")
      self.text = text
      self.parameters = self.get_parameters(text)
      self.func_name = self.get_function_name(text)

      name = uuid.uuid4()
      super().__init__(name,parent=parent,children=children,**kwargs)

  def toJSON(self):
    fun_dict = {"name":self.func_name}
    defs = [node.text for node in self.children if type(node) == Node]
    fun_dict["description"] = clean_description(" ".join(defs))
    param_nodes = [node for node in self.children if type(node) == ParameterNode]
    #TODO write own json if no parameter nodes are available in the parsing tree
    params_json = []
    for parameter in self.parameters:
      param_node = [node for node in param_nodes if parameter in re.split(r'\s*,\s*',node.parameter_name)]
      if param_node:
        params_json.append(param_node[0].toJSON())
      else:
        #TODO: get description out of self.text
        params_json.append({"name": parameter})
    fun_dict["parameters"] = params_json
    return fun_dict

  def __str__(self):
    return f"funcname: {self.func_name}\nparameters:\n"+"\n".join(self.parameters)
    
  def get_function_name(self,text):
      funcname_regex = rf"({FunctionDescriptionNode.pythonic_char}+)\s*\("
      match = re.match(funcname_regex, text)
      return match.group(1)

    #TODO use inspect module for parameters
  def get_parameters(self,text):
      param_match =  re.search("\(([^\(\)]*)\)",text)
      if not param_match:
        return []
      param_match = param_match.group(1)
      parameters = []
      if param_match:
          for param in param_match.split(","):
            param = param.split("=")[0]
            parameters.append(re.match(r"\s*\[?(\S+)",param).group(1).replace("[\[\]<>]",""))
      return parameters
        
  @staticmethod
  #TODO: match irfft2(a, s=None, axes=(-2, -1), norm=None)
  def isFunctionDescription(text):
      return re.match(FunctionDescriptionNode.function_regex,text)

  @staticmethod
  def isConstructor(text,classname=None):
      text = text.replace("^class","").trim()
      if FunctionDescriptionNode.isFunctionDescription(text):
        node = FunctionDescriptionNode(text)
        if node.func_name == classname:
          return True
      return False