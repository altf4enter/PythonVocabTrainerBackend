# -*- coding: utf-8 -*-
"""
Created on Tue Apr 12 14:36:01 2022

@author: helen
"""
import re
import uuid
from anytree import Node


class HeadingNode(Node):

  def __init__(self,text, parent=None, children=None, **kwargs):
      #here, get name as label
      if not self.isHeading(text):
        raise Exception(f"{text} does not seem to be a heading")
      self.text = text
      #get meaning of heading (keywords like methods, functions, returns, ...)
      #self.subject
      name = uuid.uuid4()
      super().__init__(name,parent=parent,children=children,**kwargs)

  def get_subject(self,text):
    pass

  @staticmethod
  def isHeading(self,text,func_parameters):
      if re.search(":\s*",text):
        return True
        #TODO: füge heading-lines der form ----- zusammen
      elif re.search("-+",text):
        return True
      return False