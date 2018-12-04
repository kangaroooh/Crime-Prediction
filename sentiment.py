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
from stanfordcorenlp import StanfordCoreNLP
import json
from tqdm import tqdm
#%%
fnames = sorted(glob("hoteldata/ta/*"))
#%%
reviewlist = []
for fname in fnames:
    reviewlist.append(pd.read_excel(fname,usecols=[1,6,8]))
hotel_reviews = pd.concat(reviewlist)
#%%
# hotel_reviews.to_excel("combine_123.xlsx")
hotel_reviews = pd.read_excel("combine_123.xlsx")
#%%
nlp = StanfordCoreNLP("/home/r/Codes/txt-mng/stanford-corenlp-full-2018-10-05")
props={'annotators': 'sentiment','pipelineLanguage':'en','outputFormat':'json'}
#%%
def clean_comment(s):
    if isinstance(s, str) and s:
        s = s.replace(".", " ").strip(". ")
        return s + ". "
    return "neutral"

titles = hotel_reviews["Review Title"].apply(clean_comment)
contents = hotel_reviews["Review Content"].apply(clean_comment)
#%%
tqdm.pandas(desc="my bar!")
#%%
results_title = []
for comment in tqdm(titles):
    results_title.append(json.loads(nlp.annotate(comment, properties=props))['sentences'][0]['sentiment'])
#%%
def get_sentiment(comment):
    return json.loads(nlp.annotate(comment, properties=props))['sentences'][0]['sentiment']
result_title_apply = titles.apply(get_sentiment)
#%%
pd.Series(results_title).to_excel("title_sentiment.xlsx")
#%%
results_content = []
for comment in tqdm(contents):
    results_content.append(json.loads(nlp.annotate(comment, properties=props))['sentences'][0]['sentiment'])
pd.Series(results_content).to_excel("content_sentiment.xlsx")
#%%
ado = nlp.annotate(testa, properties=props)
#%%
res = json.loads(nlp.annotate(test, properties=props))['sentences']
#%%

nlp.close()
#%%
text = 'Horrible, dirty. ' \
       'GDUFS is active in a full range of international cooperation and exchanges in education. '


a = json.loads(nlp.annotate(text, properties=props))

#nlp.close() # Do not forget to close! The backend server will consume a lot memery.