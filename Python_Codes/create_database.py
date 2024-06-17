import sqlite3 as lite

class database:
    
    def __init__(self, db_name):
         self.db_name = db_name

    def create_database(self):
            connection = lite.connect(self.db_name)
            cursor = connection.cursor()
            cursor.execute(""" CREATE TABLE IF NOT EXISTS News(
                       Date TEXT,
                       Article TEXT
                    )""")
    
            connection.commit()
            connection.close()
    
    def dataframe_to_db(self,df,name):
        connection = lite.connect(self.db_name)
        cursor = connection.cursor()

        df.to_sql(name,connection,if_exists='replace',index=True)
        connection.commit()
        connection.close()

         
            


          
