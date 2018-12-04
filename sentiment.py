#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  4 11:23:06 2018

@author: r
"""
import pandas as pd
from glob import glob
import openpyxl
import xlrd
#%%
fnames = glob("hoteldata/ta/*")
#%%
reviewlist = []
for fname in fnames:
    reviewlist.append(pd.read_excel(fname,usecols=[1,6,8]))
hotel_reviews = pd.concat(reviewlist)
#%%

# Simple usage
from stanfordcorenlp import StanfordCoreNLP
import json
#%%
nlp = StanfordCoreNLP("/home/r/Codes/txt-mng/stanford-corenlp-full-2018-10-05")

#%%
text = 'Horrible, dirty. ' \
       'GDUFS is active in a full range of international cooperation and exchanges in education. '

props={'annotators': 'sentiment','pipelineLanguage':'en','outputFormat':'json'}
a = json.loads(nlp.annotate(text, properties=props))

#nlp.close() # Do not forget to close! The backend server will consume a lot memery.