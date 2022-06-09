# -*- coding: utf-8 -*-
"""
Created on Tue Apr 12 21:50:54 2022

@author: helen
"""

from pymongo import MongoClient

import importlib

import types
from anytree import RenderTree

import json
import sys
import io
import pytz
from Package import Package
import datetime

client = MongoClient("mongodb://localhost:2717/")

#client.drop_database('packages')

#client (mongodb) -> client.<db> (database) -> db.<coll> (collection)
db = client.python_vocab_trainer

#result=db['packages'].insert_one(json)

#db.packages.find_one({'packages.name':'ijson.backends'})['packages'][0]['classes'][0]

#TODO make in tree structure
def save_to_database(package_instance):
    #delete old entry if existing
    db['packages'].delete_one({"name": package_instance.__name__})
    db['updates'].delete_one({"name":package_instance.__name__})
    print(f"getting package elements of package {package_instance.__name__}")
    package = Package(package_instance)
    print("creating json of package information")

    package.set_help_strings()
    package.set_descriptions()
    #TODO get descriptions of strings
    jsn = package.toJSON()
    #TODO probleme bei encoding von json im frontend
    jsn['updated'] = str(datetime.datetime.now())
    with open('C:/Users/helen/Desktop/tmp/json.json', 'w') as f:
        json.dump(jsn, f)
    result=db['packages'].insert_one(jsn)
    result =db['updates'].insert_one({"name": package.name, "updated": datetime.datetime.utcnow()})
    

import matplotlib
import functionDescriptionNode
import anytree
import imageio
#probleme bei
import cryptography
import ijson
import _io

import math
#db['packages'].delete_one({"name": 'dummy-package'})

save_to_database(math)

#print(db.list_collection_names())

#print(client.list_database_names())


jsn = {
    "name": "dummy-package",
    "id":"ABC",
    "functions": [
        {
        "name": "add",
        "id":"CDF",
        "parameters":[
            {"name": "a",
            "id":"WOE",
            "description": "The first summand."},
            {"name": "b",
                "id":"DPFE",
            "description":"The second summand."}],
        "description": "Adds two numbers together"
        }
    ],
    "classes": [
        {"name":"Object",
        "description":"Is an object.",
        "id":"ALS",
        "functions":[
            {"name":"call",
            "id":"SDED",
            "parameters":[],
            "description":"calls the function"}
        ]}
    ]
}

#result=db['packages'].insert_one(jsn)




