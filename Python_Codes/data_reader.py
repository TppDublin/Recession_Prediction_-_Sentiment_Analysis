import create_database as db
import news_pdf_scraper as Ns
import Fred_data as Fd
import pandas as pd
import os
import glob
import fitz

# Creating Database
db_name = 'Recession_new.db'
data_base_obj = db.database(db_name)
#db.update_quer()

# Fetching data from Fred 
#---------------------------------------------------------------------------------------

base_url = "https://api.stlouisfed.org/fred/"
obs_endpoint = "series/observations"
key = 'Input required key from FRED '
series_id= ['USREC','UNRATE','T10Y2Y','USEPUINDXD']
ticker = '^SPX'
start_date = '2005-12-01'
end_date = '2023-12-01'
obj = Fd.Fred(base_url,key,obs_endpoint,series_id,ticker,start_date,end_date)
fred_data = obj.fred_data()
fred_data.to_csv('fred_data.csv')
data_base_obj.dataframe_to_db(fred_data,"Quant_Data")
#-------------------------------------------------------------------------------------------

# Fetching news article 
ref_date = obj.yfinance()
dfs = []
keywords = ['']
# Access the files from directory
path = r'your path'
data = glob.glob(os.path.join(path, '*.pdf'))
i=0
for pdf_files in data:
    document  = fitz.open(pdf_files)
    obj = Ns.News_call(document,str(ref_date.index[i]))
    df = obj.fetch_data()
    dfs.append(df)
    i+=1
News_data = pd.concat(dfs, ignore_index=True)
data_base_obj.dataframe_to_db(News_data,'News_Data')


#final_df.rename(index = {'index':'Date'},inplace=True)
#final_df.to_csv('key.csv')
#final_df['Sum'] = final_df[['recession','uncertainty','crisis','unemployment']].sum(axis=1)
#db.create_db_dataframe(final_df,'Keywords')

