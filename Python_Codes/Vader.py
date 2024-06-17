import pandas as pd 
import sqlite3 as lite
import nltk
import re
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import create_database as db

class Text_analysis:
    
    def __init__(self,table_name,thresold):
        self.table_name = table_name
        self.thresold = thresold
      
    def query(self): 
        connection = lite.connect("Recession_new.db")
        q= f"SELECT * FROM {self.table_name}"    
        df = pd.read_sql_query(q,connection)
        df = df.drop(columns=['index'],axis=1)
        df['Date'] = pd.to_datetime(df['Date'])
        return df 
    
    def vader_analyzer(self):
        
        temp_data_store = pd.DataFrame()
        count = 0
        data = obj.query()
        unique_date = data['Date'].unique()
        Lm = WordNetLemmatizer()
        sid = SentimentIntensityAnalyzer()
        compound_senti = []
        dates = [] 

        for date in unique_date:
            
            positive_count = 0
            neutral_count = 0
            negative_count = 0

            date = str(date).split(" ")
            quater_data = data[data['Date'] == pd.to_datetime(date[0])]
            quater_data = quater_data.reset_index()
            
            print("Processing News article for quater :", date[0])
            
            for i in range(len(quater_data)):
                
                text = quater_data['Article'][i]
                filter_text = re.sub('Document\s+[A-Z]+\d+[a-zA-Z\d]+$','',text)
                sentiment = sid.polarity_scores(filter_text)
                #print(sentiment)
                compound_senti.append(sentiment['compound'])
                dates.append(date[0])

                if sentiment['compound'] > self.thresold:
                    positive_count += 1
                elif sentiment['compound'] < -(self.thresold):
                    negative_count += 1
                else:
                    neutral_count += 1

            temp_dict = {'Date': date[0], 
                        'positive': positive_count,
                        'neutral': neutral_count,
                        'negative': negative_count}
            
            temp_data = pd.DataFrame(temp_dict,index = [count])
            temp_data_store = pd.concat([temp_data_store,temp_data])
            count +=1
       
        # For checking the distribution of "compound", polarity output

        temp = {'Date':dates,'Polarity_compound':compound_senti}
        temp_df = pd.DataFrame(temp)

        
        return temp_df,temp_data_store


db_name = 'Recession_new.db'
table_name = "Fomc_Data"
thresold = 0.5

data_base_obj = db.database(db_name)
obj = Text_analysis(table_name,thresold)
compound,v_senti = obj.vader_analyzer()

#data_base_obj.dataframe_to_db(v_senti,'Senti')
#data_base_obj.dataframe_to_db(compound,'Basic_compound')


