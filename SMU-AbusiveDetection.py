import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="XXX"

from google.cloud import translate
client = translate.Client()
    
import paralleldots
import json
paralleldots.set_api_key("XXX")

import sys
import jsonpickle

import time

import pyodbc 
conn = pyodbc.connect(XXX)

cursor = conn.cursor()

import string
import re,string

def strip_links(text):
    link_regex    = re.compile('((https?):((//)|(\\\\))+([\w\d:#@%/;$()~_?\+-=\\\.&](#!)?)*)', re.DOTALL)
    links         = re.findall(link_regex, text)
    for link in links:
        text = text.replace(link[0], ', ')    
    return text

def strip_all_entities(text):
    entity_prefixes = ['@','#',';','.','!','?']
    #entity_prefixes = [';']
    
    for separator in  string.punctuation:
        if separator not in entity_prefixes :
            text = text.replace(separator,' ')
    words = []
    for word in text.split():
        word = word.strip()
        if word:
            if word[0] not in entity_prefixes:
                words.append(word)
    return ' '.join(words)

from googletrans import Translator
translator = Translator()

import pandas as pd 
data = pd.read_csv('smu_clean.csv', sep=",", engine='python')

# read row line by line
for d in data.values:

    # Wait for 2 seconds
    time.sleep(2) 
    
    full_text=str(d[5]).replace ("'","")

    #Translate (Google Translate API)
    text_translated = client.translate(full_text)['translatedText']
    
    #Emotion (Paralleldots API)
    response=paralleldots.abuse(text_translated)
    
    #print (response)
            
    Abusive = response["abusive"]
    Hate = response["hate_speech"]
    Neither = response["neither"]
            
    cursor.execute("INSERT INTO smu_processed VALUES ('" + str(d[0]) + "','" + str(d[1]) + "','" + str(d[2]) + "','" + str(d[3]) + "','" + str(d[4]) + "','" + str(d[5]).replace ("'","") + "','" + str(d[6]).replace ("'","") + "','" + str(Abusive) + "','" + str(Hate) + "','" + str(Neither) + "')")
    conn.commit()
        
conn.close()
print ("Done!")

