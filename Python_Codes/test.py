import pandas as pd 
import sqlite3 as lite
import nltk
from nltk.corpus import stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import re
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from nltk.stem import WordNetLemmatizer
import matplotlib.pyplot as plt
from nltk.corpus import sentiwordnet as swn
import create_database as db




connection = lite.connect("Recession_new.db")
q= f"SELECT * FROM {'Fomc_Data'}"    
df = pd.read_sql_query(q,connection)
df = df.drop(columns= 'index', axis=1 )

LoughranMcDonald_df =pd.read_csv('Loughran-McDonald.csv', index_col=None)
LoughranMcDonald = LoughranMcDonald_df.set_index('word')['polarity'].to_dict()

final_data = pd.DataFrame(columns=['Sentiment'])
data = []
dts = []

key_dict = {
1:['strong','robust','considerable','upbeat','brisk','surge'],
3/4:['normal','solid','steady'],
1/2:['modest','moderate','sustainable'],
1/4:['slow','gradual','subdued','muted'],
0:['unclear','mixed'],
-1/4:['decelerating','stabilizing','ongoing adjustment','leveling out'],
-1/2:['continued weakness','sluggish','slack','below potential'],
-3/4:['declining','deteriorating'],
-1:['recession','contraction','sharp','widespread decline'],
}


key_name = {1:'Strong Growth' 	
,3/4:'Normal Growth'
,1/2:'Modest Growth'
,1/4:'Slow Growth'
,0:'Neutral Unclear' 	
,-1/4:'Decelerating Growth'
,-1/2:'Continued Weakness'
,-3/4:'Decline'
,-1:'Pessimistic Recession'
}

count = 0
word_freq = {}
sentence = ""
for art in range(len(df)):
    print("Processing article :", art)
    text_d = df.loc[art,'Article']
    words = nltk.word_tokenize(text_d)
    for j in range(0,len(words)-1):
        word = re.sub('[^a-zA-Z]','',words[j])
        word = word.lower()
        if word not in stopwords.words('english'):
            for key,value in key_dict.items():
                if word in value:
                    count +=1
                    word_freq[key] = count 
                    break
        
   
    max_key = max(word_freq, key=word_freq.get)
    print(key_name[max_key])

    if word_freq =="":
        val = 0
        data.append(val)
        dts.append(df.loc[art,'Date'])
    else:
        data.append(max_key)
        dts.append(df.loc[art,'Date'])


print(len(data))
print(len(dts))

final_key = {'Date':dts, "Sentiment":data}
final_data = pd.DataFrame(final_key)


db_name = 'Recession_new.db'
table_name = "Fomc_Sentiment"
data_base_obj = db.database(db_name)
data_base_obj.dataframe_to_db(final_data,table_name)


