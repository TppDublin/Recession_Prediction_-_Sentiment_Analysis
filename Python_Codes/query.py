import sqlite3 as lite
import pandas as pd

class query:

    def get_data():
        connection = lite.connect("Recession_db.db")
        query="""select * FROM News """     
        table = pd.read_sql_query(query,connection)

        return table
    
    
            