# -*- coding: utf-8 -*-
"""
Created on Tue Apr 19 16:21:28 2022

@author: helen
"""

from nltk.tokenize import sent_tokenize
import re

def sentence_is_no_description(sent):
    if re.search(r'--',sent):
        return True
    if re.search('>>>',sent):
        return True
    return False

#TODO find missed opportunities
def clean_description(description):
    sents = sent_tokenize(description)
    descr_sents = []
    for sent in sents:
        if sentence_is_no_description(sent):
            break
        descr_sents.append(sent)
    return " ".join(descr_sents)