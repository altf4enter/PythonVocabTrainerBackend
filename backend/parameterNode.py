# -*- coding: utf-8 -*-
"""
Created on Tue Apr 12 12:24:06 2022

@author: helen
"""

import re
import uuid
from anytree import Node, RenderTree
from nltk.tokenize import word_tokenize, sent_tokenize
import string
from clean_data import clean_description

class ParameterNode(Node):

  def __init__(self,text,function_params, parent=None, children=None, **kwargs):
      #here, get name as label
      if not self.isParameterMentioned(text,function_params):
        raise Exception(f"{text} does not mention any function parameters")
      self.text = text
      self.parameter_name = self.get_parameter_name(function_params)
      name = uuid.uuid4()
      super().__init__(name,parent=parent,children=children,**kwargs)
  
  def get_parameter_name(self,function_params):
    parameter_names = []
    words = ParameterNode.get_possible_parameter_words(self.text)
    for param in function_params:
        for word in words:
            if ParameterNode.parameter_name_compare(param,word):
                parameter_names.append(param)
    return ", ".join(parameter_names)

  def toJSON(self):
    param_json = {"name": self.parameter_name}
    defs = [node.text for node in self.children if type(node) == Node]
    param_json["description"] = " ".join(defs)
    return param_json
  
  @staticmethod
  def parameter_name_compare(param1,param2):
      param1 = param1.translate(str.maketrans('', '', string.punctuation))
      param2 = param2.translate(str.maketrans('', '', string.punctuation))
      if not param1 or not param2:
          return False
      return param1 == param2
  
  @staticmethod
  def get_possible_parameter_words(text):
      words = word_tokenize(text)
      if re.match(r'^\S+(,\s*\S+)+', text):
          last_index_of_comma = len(words) - 1 - words[::-1].index(',')
          words = words[:last_index_of_comma+1]
      else:
          words = [words[0]] 
      return words

  @staticmethod
  def isParameterMentioned(text,func_parameters):
      words = ParameterNode.get_possible_parameter_words(text)
      for param in func_parameters:
          for word in words:
              if ParameterNode.parameter_name_compare(param,word):
                  return True
      return False

