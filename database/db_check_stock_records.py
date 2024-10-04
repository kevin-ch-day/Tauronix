import pandas as pd
from . import db_connection as db

def analyze_records(connection):
    try:
        query = """
            SELECT *, COUNT(*) AS count 
            FROM stock_data 
            GROUP BY CompanyID, Date, Open, High, Low, Close, AdjClose, Volume 
            HAVING count > 1
        """
        result = db.execute_query(connection, query)
        if result:
            columns = ["CompanyID", "Date", "Open", "High", "Low", "Close", "AdjClose", "Volume", "Count"]
            df_duplicates = pd.DataFrame(result, columns=columns)
            return df_duplicates
        else:
            print("No duplicate rows found.")
            return pd.DataFrame()
        
    except Exception as e:
        print("Error while checking for duplicate rows:", e)
        return pd.DataFrame()

def remove_duplicate_rows(connection, df_duplicates):
    try:
        if not df_duplicates.empty:
            print(f"{len(df_duplicates)} duplicate rows found. Removing duplicate rows...")
            for index, row in df_duplicates.iterrows():
                delete_query = """
                    DELETE FROM stock_data 
                    WHERE CompanyID=%s AND Date=%s AND Open=%s AND High=%s AND Low=%s AND Close=%s AND AdjClose=%s AND Volume=%s
                """
                data = (row["CompanyID"], row["Date"], row["Open"], row["High"], row["Low"], row["Close"], row["AdjClose"], row["Volume"])
                if db.delete_data(connection, delete_query, data):
                    print(f"Deleted duplicate row: {row['CompanyID']}, {row['Date']}")
                else:
                    print(f"Failed to delete duplicate row: {row['CompanyID']}, {row['Date']}")
            
            print("Duplicate rows removed successfully.")
        
        else:
            print("No duplicate rows found.")

    except Exception as e:
        print("Error while removing duplicate rows:", e)

def check_for_duplicate_rows():
    print("Checking For Duplicate Stock Records..")
    conn = db.create_connection()
    if conn:
        try:
            df_results = analyze_records(conn)
            if not df_results.empty:
                remove_duplicate_rows(conn, df_results)
            
        finally:
            db.close_connection(conn)
    else:
        print("Unable to establish database connection.")