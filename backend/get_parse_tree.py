# -*- coding: utf-8 -*-
"""
Created on Tue Apr 12 12:56:46 2022

@author: helen
"""

import re
import uuid
from nltk.tokenize import word_tokenize, sent_tokenize
from anytree import Node, RenderTree, LevelOrderIter
from functionDescriptionNode import FunctionDescriptionNode#
from parameterNode import ParameterNode
from classNode import ClassNode

pythonic_char = r"[A-Za-z0-9\_/\*<>]"
#TODO (a,a,a,a,a,...) als funktionsparameter
#TODO <> als optionale werteparameter
parameter_init = rf"(\s*|{pythonic_char}+|\S+\s*=\s*\(\s*(\s*\S+\s*,?)\s*\)|\[\s*{pythonic_char}+\s*\]|{pythonic_char}+\s*=\s*[^,]+|(\*args)|(\*\*kwargs)|/|\.+)"
parameter_init = "("+"|".join(["\s*","{pythonic_char}+",""]) + ")"
function_regex = rf"{pythonic_char}+\s*\((\s*{parameter_init}\s*,?)+\)"

def post_process(text):
    #TODO ist bisschen speziell
    pattern = re.compile("\s\|\s\s")
    matches = pattern.findall(text)
    if len(matches) > 2:
        text = text.replace("|","")
    return text

#returns a dictionary with indentation levels for each line
def mark_line_indentation_levels(lines):
    lines_parsed = []
    indentation_markers = [""]
    indentation_level=0
    for line in lines:
        if re.match("^\s*$",line):#if line is empty
            continue
        #if a new identation marker is recognized
        elif re.match("^"+"".join(indentation_markers)+"\s+\S",line):
            match = re.match("^"+"".join(indentation_markers)+"(\s+)",line)
            indentation_markers.append(match[1])
            indentation_level+=1
            lines_parsed.append({"text":line.strip(),"level":indentation_level})
            continue
        for marker_level in range(len(indentation_markers)):
            if re.match("^"+"".join(indentation_markers[:marker_level+1])+"\S",line):
                lines_parsed.append({"text":line.strip(),"level":marker_level})
                indentation_level = marker_level
                break
    return lines_parsed


def get_indentation_children(lines_and_indentations,level=0):
    children = []
    level_idxs = [line_idx for line_idx,line in enumerate(lines_and_indentations) if line['level'] == level]
    for idx,line_idx in enumerate(level_idxs):
        line = lines_and_indentations[line_idx]
        if line_idx == len(lines_and_indentations)-1:
            children.append(Node(name=uuid.uuid4(),text=line['text']))
            continue
        next_line = lines_and_indentations[line_idx+1]
        if next_line['level'] == level:
            children.append(Node(name=uuid.uuid4(),text=line['text']))
        if next_line['level'] > level:
            next_level_lines = []
            if idx == len(level_idxs)-1:#if all the next list elements are on the next level
                next_level_lines = lines_and_indentations[line_idx+1:]
            else:
                next_level_lines = lines_and_indentations[line_idx+1:level_idxs[idx+1]]
            rec_children = get_indentation_children(next_level_lines,
                                                   level=next_line['level'])
            children.append(Node(name=uuid.uuid4(),text=line['text'],children=rec_children))
    return children
        

def parse_indentation_tree(lines_and_indentations):
    #return the children of the tree
    return Node("root",children=get_indentation_children(lines_and_indentations),text="")

#TODO if parent is empty string but child is not empty, search last parent
def delete_empty_children(children):
  new_children = []
  for child in children:
    if child.children is not None:
      child.children = delete_empty_children(child.children)
    if not re.match("^\s*$",child.text):
      new_children.append(child)
  return new_children
    
def delete_empty_nodes(tree):
  if tree.children is not None:
    tree.children = delete_empty_children(tree.children)
  return tree

#TODO: first functions, then parameters? or what to do with classes
def replace_function_nodes(tree,classname=None):
  return replace_function_nodes_children([tree],classname=classname)[0]
  
def replace_function_nodes_children(nodes,classname=None):
  new_nodes = []
  for node in nodes:
    new_node = Node(name=uuid.uuid4(),text=node.text)
    if FunctionDescriptionNode.isFunctionDescription(node.text): 
      new_node = FunctionDescriptionNode(node.text)
    if node.children is not None:
      new_node.children = replace_function_nodes_children(node.children,classname=classname)
    new_nodes.append(new_node)
  return new_nodes

def replace_class_nodes(tree,classname=None):
  return replace_class_nodes_children([tree],classname=classname)[0]
  
def replace_class_nodes_children(nodes,classname=None):
  new_nodes = []
  for node in nodes:
    new_node = node
    if ClassNode.isClassDescription(node.text, classname=classname):
      new_node = ClassNode(node.text, classname=classname)
    if node.children is not None:
      new_node.children = replace_class_nodes_children(node.children,classname=classname)
    new_nodes.append(new_node)
  return new_nodes

#now detect parameter nodes
def replace_parameter_node_children(children,functionDescriptionParent=None):
  new_children = []
  for child in children:
    if child.children:
      if isinstance(child, FunctionDescriptionNode):
        functionDescriptionParent = child
      child.children = replace_parameter_node_children(child.children,
                                                       functionDescriptionParent=functionDescriptionParent)
    if functionDescriptionParent is not None and ParameterNode.isParameterMentioned(child.text,functionDescriptionParent.parameters):
      if isinstance(child, FunctionDescriptionNode):
          new_children.append(child)
      else:
          new_children.append(ParameterNode(child.text,functionDescriptionParent.parameters,children=child.children))
    else:
      new_children.append(child)
  return new_children

def replace_parameter_nodes(tree):
  tree.children = replace_parameter_node_children(tree.children)
  return tree

"""{"name":"Object",
        "description":"Is an object.",
        "id":"ALS",
        "functions":[
            {"name":"call",
            "id":"SDED",
            "parameters":[],
            "description":"calls the function"}
        ]}

"""

#returns a cleaned tree that marks classes, functions and parameters
def get_parsed_tree(help_text,classname=None,prnt=False):
  line_indentations= mark_line_indentation_levels(
  help_text.replace("|"," ").split("\n")
  ) #TODO unsauber
  tr = parse_indentation_tree(line_indentations)
  tr = delete_empty_nodes(tr)
  tr = replace_function_nodes(tr,classname=classname)
  tr = replace_parameter_nodes(tr)
  tr = replace_class_nodes(tr,classname=classname)
  if prnt:
    for pre,_,node in RenderTree(tr):
      print(pre,type(node).__name__,node.text)
  return tr