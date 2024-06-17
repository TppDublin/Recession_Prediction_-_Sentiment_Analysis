import pandas as pd 
import sqlite3 as lite
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

class sentiment:

    def __init__(self,table_name,sentiment):
        self.table_name = table_name
        self.sentiment = sentiment

    def analyze(self):
        
        connection = lite.connect("Recession_new.db")
        q= f"SELECT * FROM {self.table_name}"    
        df = pd.read_sql_query(q,connection)
        df = df.drop(columns= 'index', axis=1 )

        quant = "SELECT * FROM Quant_Data"
        q_df = pd.read_sql_query(q,connection)

        return df,q_df

   

    def sentiment_image(self):
        df,q_df = self.analyze()    
         
        f, ax = plt.subplots(figsize=(18,15))

        sns.barplot(x="Date", y="positive", data=df,
            label="Positive",color=sns.color_palette("viridis",40)[35])
        
        sns.barplot(x="Date", y="negative", data=df,
                label="Negative",color=sns.color_palette("viridis",40)[25])

        sns.barplot(x="Date", y="neutral", data=df,
            label="Neutral",color=sns.color_palette("viridis",40)[8])

        # Add a legend and informative axis label
        ax.legend(ncol=3, loc="upper right", frameon=True, fontsize=20)
        ax.set(xlim=(0, len(df)), ylabel="",
                xlabel="")
        
        ax.set_xlabel("Sentiment Count per Quarter", fontsize=20)
        ax.set_ylabel("Frequency", fontsize=20)
        
        n = 4 
        ticks_to_show = [df['Date'][i] if i % n == 0 else '' for i in range(len(df['Date']))]
        plt.xticks(range(len(df['Date'])), ticks_to_show, rotation=45, fontsize=16)

        sns.despine(left=True, bottom=True)

    def pie_chart(self):
        df, q_df = self.analyze()

        time = ['2008-12-31','2016-12-31','2020-06-30']

        for i in time:
            data = df[df['Date'] == i]
            data= np.array(data.iloc[:,1:])
        
            plt.figure(figsize=(6, 6))
            plt.pie(data[0], labels=['positive','neutral','negative'], autopct='%1.1f%%', startangle=140, colors=sns.color_palette('viridis'), explode=(0.1, 0, 0))
            plt.axis('equal')  
            plt.title(i)
            plt.show()

      
        
    def image_compound(self):
        df,q_df = self.analyze()
        plt.figure(figsize=(8, 6))
        sns.histplot(df['Polarity_compound'], bins=10, kde=True, color='skyblue')
        plt.title('Distribution of Compound Scores')
        plt.xlabel('Compound Score')
        plt.ylabel('Frequency')
        plt.tight_layout()
        plt.show()
        
    def proportion(self):
        df,q_df = self.analyze()
        df['proportion'] = df['negative']/df['positive']
        df['Increment/Decrement_rate'] = df['proportion'] - df['proportion'].shift(1)
        #df['Sentiment'] = 0
        #df.loc[df['Increment/Decrement_rate'] <0, 'Sentiment'] = 1
        #print(df['Increment/Decrement_rate'].mean())
        
        f, ax = plt.subplots(figsize=(18,10))

        sns.barplot(x="Date", y="proportion", data=df,color=sns.color_palette("viridis",40)[25], linewidth=2,label = 'Negative per positive article')
        #sns.lineplot(x="Date", y="Increment/Decrement_rate", data=df, color='blue', linestyle='--', label ='Positive sentiment increment/decrement rate')

        n = 4 
        ticks_to_show = [df['Date'][i] if i % n == 0 else '' for i in range(len(df['Date']))]
        plt.xticks(range(len(df['Date'])), ticks_to_show, rotation=45, fontsize=16)
        plt.axhline(y=0.2, color='black', linestyle='-', label = 'Threshold',linewidth=2)

        ax.legend(ncol=3, loc="upper right", frameon=True, fontsize=20)

        plt.title(f'Publication of negative sentiment artice per positive sentiment', fontsize=18)
        plt.xlabel('Dates', fontsize=20)
        plt.ylabel('Proportion', fontsize=20)
        plt.tight_layout() 
        plt.show()
        

    def fomc_sentimen(self):
        df,q_df = self.analyze()
        f, ax = plt.subplots(figsize=(18,15))
        plt.plot(df['Date'], df['Sentiment'],color=sns.color_palette("viridis",40)[8],linewidth=3)
        n= 4
        ticks_to_show = [df['Date'][i] if i % n == 0 else '' for i in range(len(df['Date']))]
        #print(len(ticks_to_show))
        plt.ticks(fontsize =16)
        plt.xticks(ticks_to_show, rotation=45, fontsize=16)
        plt.title("Sentiment of FOMC", fontsize = 16)
        plt.xlabel('Dates', fontsize=20)
        plt.ylabel('Sentiment Score', fontsize=20)
        plt.plot()

        #sns.barplot(x="Date", y="Sentiment", data=df,color=sns.color_palette("viridis",40)[25], linewidth=2,label = 'Negative per positive article')
        #return df

#txts = ['negative','neutral','positive']
#for txt in txts:
obj = sentiment('Senti','negative')
obj.proportion()
#df
#df
#obj.proportion()

