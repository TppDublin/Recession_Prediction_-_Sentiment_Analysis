import pandas as pd
import re

class News_call:

    def __init__(self,file,date):
        self.file = file
        self.date = date

    def fetch_data(self):
        
        count = 0
        counter = 0
        headline_list = []
        article_list = []
       
        print("Processing News article for quaterly date :", self.date )
        for page in self.file:

            text = page.get_text()
            pattern_1 = r"\b[A-Z][a-z]+\s[A-Z][a-z]+\b.*?\b\d+\s+words\b"
            pattern_2 = "Dow Jones & Company"

            if re.search(pattern_2.lower(),text.lower(),re.DOTALL) or re.search(pattern_1,text,re.DOTALL):
                if count > 0:
                    article_list.append(article)
                elif count == 0 and  counter == 1:
                    counter = 0
                    article_list.append(article)
                else:
                    count = 0

                article = ""

                blocks = page.get_text("blocks")
                for content in blocks:
                    if content[5] == 1:
                        headline = content[4]
                        #print(headline)
                        headline_list.append(headline)
                    if content[5] > 2:
                        article += content[4]
                counter = 1
            
            else:
                count+=1
                blocks = page.get_text("blocks")
                for content in blocks:
                    if content[5] > 0:
                        article += content[4]
        article_list.append(article)
        
        print(len(headline_list))
        value = {'Date' : self.date,
                 'Headline':headline_list,
                 'Article': article_list 
                }
        
        news_dataframe = pd.DataFrame(value)
        print("Size of News artice", news_dataframe.shape[0])
        return news_dataframe     
