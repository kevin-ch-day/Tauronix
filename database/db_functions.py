import pandas as pd
import datetime

from . import db_connection as db

def get_polygon_api_key():
    # Retrieve the Polygon API key from the database and update the last_used timestamp.
    
    query_select_key = """
        SELECT api_key FROM polygon_api_keys
        ORDER BY last_used IS NULL DESC, last_used ASC
        LIMIT 1;
    """
    
    query_update_last_used = """
        UPDATE polygon_api_keys
        SET last_used = CURRENT_TIMESTAMP
        WHERE api_key = %s;
    """
    
    try:
        connection = db.create_connection()
        if connection:
            result = db.execute_query(connection, query_select_key)
            
            if result:
                api_key = result[0][0]

                # Update the last_used timestamp for the selected key
                #cursor_update = db.execute_query(connection, query_update_last_used, api_key)
                
                return api_key
                
            else:
                print("No API key found.")
                db.close_connection(connection)
                return None
        else:
            print("Error: Unable to establish database connection.")
            return None
    except Exception as e:
        print(f"Error retrieving API key: {e}")
        return None

def retrieve_company_info():
    # Retrieve company information from the database.

    query = "SELECT CompanyID, CompanyName, Location, StockSymbol FROM company_info ORDER BY CompanyID"
    try:
        connection = db.create_connection()
        if connection:
            result = db.execute_query(connection, query)
            db.close_connection(connection)
            if result:
                columns = ["CompanyID", "CompanyName", "Location", "StockSymbol"]
                df = pd.DataFrame(result, columns=columns)
                return df
            else:
                print("No data found.")
                return None
        else:
            print("Error: Unable to establish database connection.")
            return None
    except Exception as e:
        print("Error:", e)
        return None

def retrieve_company_disclosure_dates():
    """Retrieve company disclosure dates from the database."""
    query = """
        SELECT a.CompanyID AS ID,
               a.CompanyName AS Name,
               a.StockSymbol AS Symbol,
               b.DisclosureDate AS `Disclosure Date`
        FROM company_info a
        JOIN data_breach_disclosures b ON b.CompanyID = a.CompanyID
        ORDER BY b.DisclosureDate
    """
    try:
        connection = db.create_connection()
        if connection:
            result = db.execute_query(connection, query)
            db.close_connection(connection)
            if result:
                columns = ["ID", "Name", "Symbol", "Disclosure Date"]
                df = pd.DataFrame(result, columns=columns)
                return df
            else:
                print("No data found.")
                return None
        else:
            print("Error: Unable to establish database connection.")
            return None
    except Exception as e:
        print("Error:", e)
        return None

def retrieve_stock_data():
    # Retrieve all stock data from the database ordered by CompanyID.

    query = "SELECT * FROM stock_data ORDER BY CompanyID, Date"
    try:
        connection = db.create_connection()
        if connection:
            result = db.execute_query(connection, query)
            db.close_connection(connection)
            if result:
                columns = ["CompanyID", "Date", "Open", "High", "Low", "Close", "AdjClose", "Volume"]
                df = pd.DataFrame(result, columns=columns)
                return df
            else:
                print("No data found.")
                return None
        else:
            print("Error: Unable to establish database connection.")
            return None
    except Exception as e:
        print("Error:", e)
        return None

def retrieve_dow_jones_data():
    # Retrieve Dow Jones data from the database.

    query = "SELECT * FROM dow_jones ORDER BY Date"
    try:
        connection = db.create_connection()
        if connection:
            result = db.execute_query(connection, query)
            db.close_connection(connection)
            if result:
                columns = ["Date", "Price", "Open", "High", "Low", "Volume", "Change_Percent"]
                df = pd.DataFrame(result, columns=columns)
                return df
            else:
                print("No data found.")
                return None
        else:
            print("Error: Unable to establish database connection.")
            return None
    except Exception as e:
        print("Error:", e)
        return None

def retrieve_stock_price_and_dow_jones_data(company_ids=None):
    # Retrieve combined data from multiple tables, with an optional filter for specific company IDs.

    # Base query
    query = """
        SELECT x.CompanyID 'Company ID',
               x.CompanyName 'Company Name',
               y.Date,
               y.Open 'Stock Open',
               y.High 'Stock High',
               y.Close 'Stock Close',
               y.Volume 'Stock Volume',
               z.Price 'Dow Jones Price',
               z.Open 'Dow Jones Open',
               z.High 'Dow Jones High',
               z.Low 'Dow Jones Low',
               z.Volume 'Dow Jones Volume',
               z.Change_Percent 'Dow Jones Change %'
        FROM company_info x
        JOIN stock_data y ON y.CompanyID = x.CompanyID
        JOIN dow_jones z ON z.Date = y.Date
    """
    
    # Add WHERE clause if company_ids are provided
    if company_ids:
        placeholders = ', '.join(['%s'] * len(company_ids))  # Prepare placeholders for IN clause
        query += f" WHERE x.CompanyID IN ({placeholders})"
    
    # Complete query with ORDER BY clause
    query += " ORDER BY y.Date, x.CompanyID;"
    
    try:
        connection = db.create_connection()
        if connection:
            cursor = connection.cursor(dictionary=True)
            # Execute query with or without company_ids
            if company_ids:
                cursor.execute(query, tuple(company_ids))  # Pass company_ids as query parameters
            else:
                cursor.execute(query)
            
            result = cursor.fetchall()
            db.close_connection(connection)
            
            if result:
                columns = ["Company ID", "Company Name", "Date", "Stock Open", "Stock High", "Stock Close", "Stock Volume",
                           "Dow Jones Price", "Dow Jones Open", "Dow Jones High", "Dow Jones Low", "Dow Jones Volume",
                           "Dow Jones Change %"]
                df = pd.DataFrame(result, columns=columns)
                return df
            else:
                print("No data found.")
                return None
        else:
            print("Error: Unable to establish database connection.")
            return None
    except Exception as e:
        print(f"Error retrieving data: {e}")
        return None


def get_company_id_by_name(company_name):
    # Retrieves the CompanyID for a given company name from the company_info table.
   
    try:
        connection = db.create_connection()
        with connection.cursor() as cursor:
            query = "SELECT CompanyID FROM company_info WHERE CompanyName = %s"
            cursor.execute(query, (company_name,))
            result = cursor.fetchone() 
            return result['CompanyID'] if result else None
    except Exception as e:
        print(f"Error retrieving Company ID: {e}")
        return None
    finally:
        if connection:
            connection.close()

def get_company_id_and_name_by_symbol(stock_symbol):
    # Retrieve the CompanyID and CompanyName based on the stock symbol.

    try:
        connection = db.create_connection()
        if connection:
            with connection.cursor() as cursor:
                query = "SELECT CompanyID, CompanyName FROM company_info WHERE StockSymbol = %s"
                cursor.execute(query, (stock_symbol,))
                result = cursor.fetchone()

                if result:
                    company_id, company_name = result[0], result[1]
                    return {"CompanyID": company_id, "CompanyName": company_name}
                else:
                    print(f"No company found for stock symbol: {stock_symbol}")
                    return None
    except Exception as e:
        print(f"Error retrieving Company ID and Name: {e}")
        return None
    finally:
        if connection:
            connection.close()

def get_company_stock_record_on_date(company_id, date):
    # Retrieves stock data for a specific company on a given date.
    
    if isinstance(date, datetime.datetime):
        date = date.strftime('%Y-%m-%d')

    query = """
        SELECT 
            x.CompanyID 'Company ID',
            x.CompanyName 'Company Name',
            y.Date,
            y.Open 'Stock Open',
            y.High 'Stock High',
            y.Close 'Stock Close',
            y.Volume 'Stock Volume',
            z.Price 'Dow Jones Price',
            z.Open 'Dow Jones Open',
            z.High 'Dow Jones High',
            z.Low 'Dow Jones Low',
            z.Volume 'Dow Jones Volume',
            z.Change_Percent 'Dow Jones Change %'
        FROM company_info x
        JOIN stock_data y ON y.CompanyID = x.CompanyID
        JOIN dow_jones z ON z.Date = y.Date
        WHERE x.CompanyID = %s AND y.Date = %s
        ORDER BY y.Date, x.CompanyID;
    """
    try:
        connection = db.create_connection()
        with connection.cursor() as cursor:
            cursor.execute(query, (company_id, date))
            result = cursor.fetchone()  # Fetch the first row
            if result:
                return dict(result)
            else:
                print(f"No data found for Company ID {company_id} on {date}.")
                return None
    except Exception as e:
        print(f"Error retrieving stock data: {e}")
        return None
    finally:
        if connection:
            connection.close()