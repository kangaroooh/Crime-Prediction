#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  8 18:18:20 2018

@author: r
"""
import pandas as pd
from glob import glob
from stanfordcorenlp import StanfordCoreNLP
from tqdm import tqdm
#%%
hotel_reviews = pd.read_excel("combine_123_allcols.xlsx")
title_sentiment = pd.read_excel("title_sentiment.xlsx")
hotel_reviews["Sentiment"] = title_sentiment
hotel_reviews["Hotel Name"] = hotel_reviews["Hotel Name"].apply(
    lambda x: x.strip())
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
    elif star >= 3 and sent == "Neutral":
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
neg_reviews = hotel_reviews[(hotel_reviews["Sentiment"] == "Negative") |
                            (hotel_reviews["Sentiment"] == "Verynegative")]
all_reviews = hotel_reviews["Reviewer Name"].value_counts().rename(
    "all_reviews")
#%%
user_neg = neg_reviews["Reviewer Name"].value_counts().rename("neg_reviews")
#%%
user_neg_all_table = pd.concat([all_reviews, user_neg], axis=1, sort=True)
#%%
fraud_users = user_neg_all_table[user_neg_all_table["neg_reviews"] ==
                                 user_neg_all_table["all_reviews"]]
#%%
"""
Fraud detection: Find the date difference of reviewer names
"""
hotel_reviews["Review Date"] = pd.to_datetime(hotel_reviews["Review Date"])
hotel_reviews["Reviewer Name"] = hotel_reviews["Reviewer Name"].astype(str)
maxdate_reviewer = hotel_reviews[["Reviewer Name", "Review Date"
                                  ]].groupby("Reviewer Name").max()
maxdate_reviewer.columns = ["maxdate"]
mindate_reviewer = hotel_reviews[["Reviewer Name", "Review Date"
                                  ]].groupby("Reviewer Name").min()
mindate_reviewer.columns = ["mindate"]
user_maxmindate = pd.concat([maxdate_reviewer, mindate_reviewer],
                            axis=1,
                            sort=True)
user_maxmindate[
    "datediff"] = user_maxmindate["maxdate"] - user_maxmindate["mindate"]
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


hotel_reviews["Effective Star Rating"] = hotel_reviews.apply(
    compute_effective_star_rating, axis=1)
#%%
"""
Using Effective Star Rating to validate if our Effective Star rating
is actually good by comparing it with the raw star rating
"""


def describe_eff(x):
    hotel_rates = x[[
        "Hotel Name", "Hotel Review Stars", "Effective Star Rating"
    ]].groupby("Hotel Name").mean()
    eq = hotel_rates[hotel_rates["Hotel Review Stars"] ==
                     hotel_rates["Effective Star Rating"]]
    mt = hotel_rates[hotel_rates["Hotel Review Stars"] >
                     hotel_rates["Effective Star Rating"]]
    lt = hotel_rates[hotel_rates["Hotel Review Stars"] <
                     hotel_rates["Effective Star Rating"]]
    print(len(eq), len(mt), len(lt))


#%%
"""
Feature Extraction: Finding % of negative reviews.
"""


def smi(x):
    vcount = x["Sentiment"].value_counts()
    summi = 0
    if 'Negative' in vcount:
        summi += vcount['Negative']
    if 'Verynegative' in vcount:
        summi += vcount['Verynegative']
    return summi


grouped_hotelname = hotel_reviews[["Hotel Name",
                                   "Sentiment"]].groupby("Hotel Name")
grouped_hotelname_rating = hotel_reviews[[
    "Hotel Name", "Effective Star Rating"
]].groupby("Hotel Name").mean()
negrev = grouped_hotelname.agg(smi)
allrev = grouped_hotelname.agg('count')
revs = pd.merge(negrev, allrev, on="Hotel Name")
revs.columns = ["nb_negreview", "nb_allreview"]
revs["percent_negreviews"] = revs["nb_negreview"] / revs["nb_allreview"]
#%%
"""
Make an aggregated table
"""
agg_hotel = pd.merge(
    revs, grouped_hotelname_rating.reset_index(), on="Hotel Name")
subhotel = hotel_reviews[[
    "Hotel Name", "Hotel Address", "Latitude", "Longitude"
]].drop_duplicates(subset="Hotel Name")
agg_hotel = pd.merge(
    agg_hotel, subhotel, left_on="Hotel Name", right_on="Hotel Name")
agg_hotel = agg_hotel[[
    "Hotel Name", "Hotel Address", "Effective Star Rating",
    "percent_negreviews", "Latitude", "Longitude"
]]
#%%
"""
Feature Extraction: is hotel near crime?.
"""
import re


def clean_loc(x):
    splits = x.split(" ")
    if splits[0].isdigit():
        return " ".join(splits[-2:])
    if re.findall(".+[-/].+", splits[0]):
        return " ".join(splits[-2:])
    return " ".join(splits[-2:])


hotelnames = agg_hotel["Hotel Address"]
hotelnames = hotelnames.apply(clean_loc)
agg_hotel["Hotel Address"] = hotelnames
#%%
crime = pd.read_csv("crimedata/AVG_CRIME_LOCAT_MTH38.csv")
res = pd.merge(
    agg_hotel, crime, left_on='Hotel Address', right_on='location', how='left')
#%%
import geopy.distance


def calc_distance(x):
    if pd.isna(x["Latitude_x"]) or pd.isna(x["Longitude_x"]) or pd.isna(
            x["Latitude_y"]) or pd.isna(x["Longitude_y"]):
        return None
    return geopy.distance.vincenty((x["Latitude_x"], x["Longitude_x"]),
                                   (x["Latitude_y"], x["Longitude_y"])).km


#%%
res.at[757, "Latitude_x"] = res.at[865, "Latitude_x"]
res.at[757, "Longitude_x"] = res.at[865, "Longitude_x"]
res.at[757, "Latitude_y"] = res.at[865, "Latitude_y"]
res.at[757, "Longitude_y"] = res.at[865, "Longitude_y"]
res.at[1139, "Latitude_x"] = res.at[294, "Latitude_x"]
res.at[1139, "Longitude_x"] = res.at[294, "Longitude_x"]
res.at[1139, "Latitude_y"] = res.at[294, "Latitude_y"]
res.at[1139, "Longitude_y"] = res.at[294, "Longitude_y"]
#%%
res['distance'] = res.apply(calc_distance, axis=1)
res['avg_crime_n'] = res['avg_crime_n'].fillna(0)
#%%
res.to_excel("final.xlsx")
