# -*- coding: utf-8 -*-
import random
import pandas as pd
import en_core_web_sm

defn_df = pd.read_csv("Data/Unsupervised Topic Modeling - Topic definitions.csv")

extracts_df = pd.read_csv("Data/Unsupervised Topic Modeling - Extracts.csv")
extracts_list = extracts_df['Extracts']

defn_list = []
for i in range(len(defn_df)):
    defn_list.append(defn_df['Definition'][i])
topic_list = defn_df['Topics']

nlp = en_core_web_sm.load()

#Function to return words with more than 0.5 similarity from the 150 Topics list
#Input, word to compare
def sim(W1,W2):
  token1 = nlp(W1)
  token2 = nlp(W2)

  return(token1.similarity(token2))
  
def compare(pairs,extract,topic,topic_no):
    sim_score = sim(topic,extract)
    if(sim_score>0.5):
        pairs.append({'Topics': topic_list[topic_no], 'Word':extract, 'score': sim_score})
    return pairs

def process_spacy(sent):
    pairs = []
    for k in range(len(defn_list)):
        pairs = compare(pairs,sent,defn_list[k],k)
    pairs = sorted(pairs, key=lambda x: x['score'], reverse=True)
    
    topics_10_s = []
    for i in range(len(pairs)):
        topics_10_s.append(pairs[i]['Topics'])    
        res = []
        [res.append(x) for x in topics_10_s if x not in res]
    
    return res[:10]
    
#process_spacy("Finance is the worst thing ever done to Accounting")    

