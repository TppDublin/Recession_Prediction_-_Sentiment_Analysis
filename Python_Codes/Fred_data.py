
import pandas as pd
import requests
import yfinance as yf

class Fred:

    def __init__(self,url,user_key,obs_endpoint,series_id,ticker,start_date,end_date):
        self.url = url
        self.user_key = user_key
        self.obs_endpoint = obs_endpoint
        self.series_id = series_id
        self.ticker = ticker
        self.start_date = start_date
        self.end_date = end_date


    def yfinance(self):
    
        df = yf.download(self.ticker,start='2005-01-01',end= '2024-03-01',interval='1mo')['Adj Close']
        df_quarterly = df.resample('QE').sum()/4
        df_quarterly = df_quarterly.pct_change()*100
        df_quarterly = df_quarterly['2005-12-31': '2023-12-31']
        return df_quarterly
       
    def fred_data(self):

        stock_data = self.yfinance()
        data = pd.DataFrame()
        for i in range(0,len(self.series_id)):
            obs_params = {
                'series_id': self.series_id[i],
                'api_key':self.user_key,
                'file_type':'json',
                'observation_start': self.start_date,
                'observation_end': self.end_date,
                'frequency': 'q'
            }
            
            #print(self.series_id[i])
            response = requests.get(self.url + self.obs_endpoint, params=obs_params)

            if response.status_code == 200:
                res_data = response.json()
                obs_data = pd.DataFrame(res_data['observations'])
                obs_data.rename(columns={'value':self.series_id[i]},inplace=True)
                obs_data.drop(['realtime_start','realtime_end'],axis=1,inplace=True)
                data = pd.concat([data, obs_data.set_index('date')], axis=1)
      

        data.index = stock_data.index
        final_data = pd.concat([data,stock_data],axis=1)
        final_data = final_data.rename(columns={'Adj Close': self.ticker})
        #print(final_data)
        return final_data

    

