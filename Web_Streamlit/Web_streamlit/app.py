import streamlit as st
import numpy as np
import pandas as pd
import pickle

youtube_model = pickle.load(open('algo_youtube.pkl', 'rb'))
instagram_model = pickle.load(open('algo_instagram.pkl', 'rb'))
maindataYoutube =  pd.read_csv("maindataYoutube.csv")
maindataInstagram =  pd.read_csv("maindataInstagram.csv")

age_df = pd.read_csv("age_range.csv")
category_df =  pd.read_csv("category.csv")
country_df =  pd.read_csv("country.csv")

st.title("Recommendation")

def format_gender(option):
       
    if option == 0:
        return "Male"
    elif option == 1:
        return "Female"
    else:
        return option
    
def format_age(option):
    age = age_df.loc[age_df['Encoded_Value'] == option, 'Audience_age_range'].values[0]
    return age
    
    
def format_category(option):
    content_category = category_df.loc[category_df['Encoded_Value'] == option, 'Content_category'].values[0]
    return content_category
    
    
def format_country(option):
    country = country_df.loc[country_df['Encoded_Value'] == option, 'Audience_country'].values[0]
    return country
    

target_gender = st.selectbox(label= "Select Target Gender", options= [0,1], format_func= format_gender)
platform = st.selectbox(label= "Select Platform", options= ["Instagram", "Youtube"])
category = st.selectbox(label= "Select Category", options= category_df['Encoded_Value'], format_func= format_category) # edit
budget = st.slider(label="Select Budget", min_value= 10000, max_value= 800000) #edit
min_engagement_rate = st.slider(label="Select Minimum Engagement Range", min_value= 1, max_value= 5) #edit
target_country = st.selectbox(label="Select Country" , options= country_df['Encoded_Value'],format_func= format_country ) #edit
target_age_range = st.selectbox(label="Select Target Age Range" ,options= age_df['Encoded_Value'], format_func= format_age) #edit

def filtered_influencer_youtube():
    filtered_youtubers = []
    for _,youtuber in maindataYoutube.iterrows():
        if youtuber['Engagement_rate'] >= min_engagement_rate \
                and youtuber['Majority_audience_gender'] == target_gender \
                and youtuber['Audience_country'] == target_country \
                and youtuber['Audience_age_range'] == target_age_range \
                and youtuber['Cost_per_post'] <= budget:
            filtered_youtubers.append((youtuber["YouTube_channel_name"],youtuber['Content_category'], youtuber['Cost_per_post']))

    return filtered_youtubers

def filtered_influencer_instagram():
    filtered_insta = []
    for _, insta in maindataInstagram.iterrows():
        if insta['Engagement_rate'] >= min_engagement_rate \
                and insta['Majority_audience_gender'] == target_gender \
                and insta['Audience_country'] == target_country \
                and insta['Audience_age_range'] == target_age_range \
                and insta['Cost_per_post'] <= budget:
            filtered_insta.append((insta["Influencer_insta_username"],insta['Content_category'], insta['Cost_per_post']))
           
    return filtered_insta


def get_recommendations_with_age_range_filter_youtube():
    
    filtered = filtered_influencer_youtube()
    dataset1 = [tup[:3] for tup in filtered]
    predictions = {}
    for uid, iid, category in dataset1:
        pred = youtube_model.predict(uid, iid)
        predictions[uid] = pred.est
    sorted_predictions = sorted(predictions.items(), key=lambda x: x[1], reverse=True)
    return sorted_predictions[:10]
    
def get_recommendations_with_age_range_filter_instagram():
    filtered = filtered_influencer_instagram()
    dataset1 = [tup[:3] for tup in filtered]
    predictions = {}
    for uid, iid, category in dataset1:
        pred = instagram_model.predict(uid, iid)
        predictions[uid] = pred.est
    sorted_predictions = sorted(predictions.items(), key=lambda x: x[1], reverse=True)
    return sorted_predictions[:10]
    

def checkPlatform():
    
    if platform == "Youtube":
        youtubers = get_recommendations_with_age_range_filter_youtube()
        for youtuber, rating in  youtubers:
             youtuber_name = maindataYoutube.loc[maindataYoutube['YouTube_channel_name'] == youtuber , 'channel_name'].iloc[0]
             st.success(youtuber_name + ' :thumbsup:')       
        
        
    else:
        influencers = get_recommendations_with_age_range_filter_instagram()
        for influencer, rating in influencers:
            influencer_name = maindataInstagram.loc[maindataInstagram['Influencer_insta_username'] == influencer, 'Influencer_insta_id'].iloc[0]
            st.success(influencer_name + ' :thumbsup:') 
        
    

trigger = st.button('Recommend ', on_click=checkPlatform)    