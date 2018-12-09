#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  8 18:18:20 2018

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
hotel_reviews = pd.read_excel("combine_123_allcols.xlsx")
title_sentiment = pd.read_excel("title_sentiment.xlsx")
hotel_reviews["Sentiment"] = title_sentiment
hotel_reviews["Hotel Name"] = hotel_reviews["Hotel Name"].apply(lambda x: x.strip())
#%%
"""
Compute Class for classification based on Sentiment Analysis and Review Stars
We believe that if those two don't go together, they might mess up our
analysis later, to we exclude them (making them -1)
"""
def compute_class(x):
    star = x["Review Stars"]
    sent = x["Sentiment"]
    ret = -1
    if star >= 4 and (sent == "Verypositive" or sent == "Positive"):
        ret = 1
    elif star <= 2 and (sent == "Verynegative" or sent == "Negative"):
        ret = 0
    elif star >=3 and sent == "Neutral":
        ret = 1
    else:
        ret = -1
    return ret
hotel_reviews_class = hotel_reviews.apply(compute_class, axis=1)
hotel_reviews["Class"] = hotel_reviews_class
#%%
"""
Fraud detection: using negative_reviews/all_reviews
We believe that those people who gave all negative reviews on all reviews
they might be fraud.
Result: The number is still too low. Can't justify that they are fraud
"""
neg_reviews = hotel_reviews[(hotel_reviews["Sentiment"] == "Negative") | (hotel_reviews["Sentiment"] == "Verynegative")]
all_reviews = hotel_reviews["Reviewer Name"].value_counts().rename("all_reviews")
#%%
user_neg = neg_reviews["Reviewer Name"].value_counts().rename("neg_reviews")
#%%
user_neg_all_table = pd.concat([all_reviews, user_neg], axis=1, sort=True)
#%%
fraud_users = user_neg_all_table[user_neg_all_table["neg_reviews"] == user_neg_all_table["all_reviews"]]
#%%
"""
Fraud detection: Find the date difference of reviewer names
"""
hotel_reviews["Review Date"] = pd.to_datetime(hotel_reviews["Review Date"])
hotel_reviews["Reviewer Name"] = hotel_reviews["Reviewer Name"].astype(str)
maxdate_reviewer = hotel_reviews[["Reviewer Name", "Review Date"]].groupby("Reviewer Name").max()
maxdate_reviewer.columns = ["maxdate"]
mindate_reviewer = hotel_reviews[["Reviewer Name", "Review Date"]].groupby("Reviewer Name").min()
mindate_reviewer.columns = ["mindate"]
user_maxmindate = pd.concat([maxdate_reviewer, mindate_reviewer], axis=1, sort=True)
user_maxmindate["datediff"] = user_maxmindate["maxdate"] - user_maxmindate["mindate"]
#%%
"""
Feature Extraction: ComputeEffective Star Rating, to enhance the current Star Ratings with score
from Sentiment Analysis. Due to the fact that people have their own weighting
justification. The 3 of some people might mean Neutral, while some mean bad.
"""
def compute_effective_star_rating(x):
    star = x["Review Stars"]
    sent = x["Sentiment"]
    ret = x["Review Stars"]
    if star >= 4 and (sent == "Verypositive" or sent == "Positive"):
        ret = star
    elif star <= 2 and (sent == "Verynegative" or sent == "Negative"):
        ret = star
    elif sent == "Neutral":
        ret = 3
    else:
        ret = None
    return ret
hotel_effective_star_rating = hotel_reviews.apply(compute_effective_star_rating, axis=1)
hotel_reviews["Effective Star Rating"] = hotel_effective_star_rating
#%%
"""
Using Effective Star Rating to validate if our Effective Star rating
is actually good by comparing it with the raw star rating
"""
hotel_rates = hotel_reviews[["Hotel Name", "Hotel Review Stars", "Effective Star Rating"]].groupby("Hotel Name").mean()
eq = hotel_rates[hotel_rates["Hotel Review Stars"] == hotel_rates["Effective Star Rating"]]
mt = hotel_rates[hotel_rates["Hotel Review Stars"] > hotel_rates["Effective Star Rating"]]
lt = hotel_rates[hotel_rates["Hotel Review Stars"] < hotel_rates["Effective Star Rating"]]
hotel_reviews["Hotel Name"].nunique()

#%%
"""
Finding correlation between hotel & Crime
"""
#%%
unique_hotel = hotel_reviews[["Hotel Name","Latitude","Longitude"]].groupby("Hotel Name").first()
#%%
crime_data = pd.read_csv("crimedata/2018-08-metropolitan-street.csv")
#%%
unique_hotel["Latitude"] = pd.to_numeric(unique_hotel["Latitude"], errors='coerce')
unique_hotel["Longitude"] = pd.to_numeric(unique_hotel["Longitude"], errors='coerce')
result = pd.merge(unique_hotel, crime_data, how='left', on=["Latitude","Longitude"])

#%%
"""
Feature Extraction: Finding % of negative reviews.
"""
grouped_hotelname = hotel_reviews[["Hotel Name", "Sentiment"]].groupby(
        "Hotel Name")
grouped_hotelname_rating = hotel_reviews[["Hotel Name", "Effective Star Rating"]].groupby(
        "Hotel Name").mean()
def smi(x):
    vcount = x["Sentiment"].value_counts()
    summi = 0
    if 'Negative' in vcount:
        summi += vcount['Negative']
    if 'Verynegative' in vcount:
        summi += vcount['Verynegative']
    return summi
negrev = grouped_hotelname.agg(smi)
allrev = grouped_hotelname.agg('count')
ab = pd.merge(negrev, allrev, on="Hotel Name")
ab.columns = ["nb_negreview", "nb_allreview"]
final_hotel = pd.merge(ab, grouped_hotelname_rating.reset_index(), on="Hotel Name")
final_hotel["percent_negreviews"] = final_hotel["nb_negreview"]/final_hotel["nb_allreview"]
#%%
subhotel = hotel_reviews[["Hotel Name", "Hotel Address"]].drop_duplicates(subset="Hotel Name")
#%%
final_hotel = pd.merge(final_hotel, subhotel, left_on="Hotel Name", right_on="Hotel Name")
#%%
final_hotel = final_hotel[["Hotel Name", "Hotel Address", "Effective Star Rating", "percent_negreviews"]]