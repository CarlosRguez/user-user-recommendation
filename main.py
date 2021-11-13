# -*- coding: utf-8 -*-
"""
Created Nov 2021

@author: Carlos

Collaborative Filtering
user-user algorithm (recommends an item to a user if similar users liked this item before)
"""

import os
import csv

def load_dataset(filename="reviews_example.csv"): #Load dataset
    data = []
    if filename and os.path.isfile(filename):
        csv_file = open(filename, encoding="utf-8-sig") 
        reader = csv.DictReader(csv_file)
        for row in reader:
            data.append(row)
        csv_file.close()
    return data

data_entries = []
data_entries = load_dataset()
#print(data_entries)
print('loaded dataset')

def reviewers_products(data_entries): #Asociate users and products in a dict
    reviewers = {}
    for i in range(len(data_entries)):
        reviewerID = data_entries[i]['reviewerID']
        productID = data_entries[i]['productID']
        if not reviewerID in reviewers:
            productID_list = []
        else:
            productID_list = reviewers[reviewerID]
        productID_list.append(productID)
        reviewers[reviewerID] = productID_list
    return reviewers #--> {'reviewerID': ['asin1','asin2'],...}
reviewers_products = reviewers_products(data_entries) 
#print(reviewers_products)
print('reviewers and products matched')

def compare_reviewers_products(reviewerID_1, reviewerID_2): # Create list of common items between two users
    products1 = reviewers_products.get(reviewerID_1)
    products2 = reviewers_products.get(reviewerID_2)
    samekeys = []
    for x in products1:
        for y in products2:
            if x==y:
                samekeys.append(x)
    return samekeys #--> in common ['productID','productID',...]
#print(compare_reviewers_products('A1RRX286ZRI830','A3G5KDMFNRUXHB'))

def reviewers_most_shared_products(reviewerID): #two lists: one of those similar users and another of those common products
    #to do: integrate this function in one
    def similar_reviewers(reviewerID_1): #list of reviewer and its common products
        ranking={}
        for reviewerID_2 in reviewers_products:
            if reviewerID_1 != reviewerID_2:
                common_products = compare_reviewers_products(reviewerID_1,reviewerID_2)
                if len(common_products)>0:
                    ranking[reviewerID_2] = common_products
        sort_ranking = sorted(ranking.items(), key=lambda x: x[1], reverse=True)#higher to lower coincidence
        return(sort_ranking) #--> [('reviewerID',['productID',...]),('reviewerID',['productID',...]),...]

    reviewers=[]
    for i in similar_reviewers(reviewerID):
        reviewers.append(i[0])
    products=[]
    for i in range(len(similar_reviewers(reviewerID))):
        for product in similar_reviewers(reviewerID)[i][1]:
            if product not in products:
                products.append(product)

    return (reviewers, products) #-->(['reviewerID','reviewerID',...],['productID','productID',...])
#print(reviewers_most_shared_products('A1RRX286ZRI830'))


def recommendation_similar_reviewers(reviewerID): # user-user algorithm. First recommendation of only similar users
    past_products = reviewers_products.get(reviewerID)
    recommendation = []
    
    similar_reviewers = reviewers_most_shared_products(reviewerID)[0]
    
    for similar_reviewer in similar_reviewers:
        similar_reviewer_products = reviewers_products.get(similar_reviewer)
        for product in similar_reviewer_products:
            if product not in past_products:
                recommendation.append(product)
    return recommendation

def Similar_reviewers_to_similar_reviewers(reviewerID): # Second recommendation for your similar users.
    recommendation2 = []
    similar_reviewers = reviewers_most_shared_products(reviewerID)[0]
    
    for similar_reviewer in similar_reviewers:
        #print(similar_reviewer,'-->',recommendation_similar_reviewers(similar_reviewer))
        recomendation = recommendation_similar_reviewers(similar_reviewer)
        for product in recomendation:
            if product not in recommendation2:
                recommendation2.append(product)
            #if len(recommendation2)>40: #depending on the dataset it may take a while, so here we limit the amount
            #    break
        #if len(recommendation2)>40:
        #    break
    return recommendation2

example_ID = 'A1RRX286ZRI830'

print('     Similar reviewers: ', reviewers_most_shared_products(example_ID)[0])
print('     All have reviews of: ', reviewers_most_shared_products(example_ID)[1])
print('     PRODUCT RECOMMENDATION 1: Similar reviewers also have reviews of:', recommendation_similar_reviewers(example_ID))
print('     PRODUCT RECOMMENDATION 2: Similar reviewers of the similar reviewers also have reviews of:', Similar_reviewers_to_similar_reviewers(example_ID))
