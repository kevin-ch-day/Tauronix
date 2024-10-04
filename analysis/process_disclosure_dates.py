# process_disclosure_dates.py

import pandas as pd
import datetime
from database import db_functions
from utils import utils_func

def handle_market_closure(disclosure_date, company_id, company_name):
    """
    Checks if the market was closed on the given date and prepares responses for closed and next open market days.
    """
    disclosure_date = disclosure_date.date() if isinstance(disclosure_date, datetime.datetime) else disclosure_date
    market_closed, reason = utils_func.is_market_closed(disclosure_date)
    responses = []
    
    if market_closed:
        # Record for the actual closure day
        responses.append({
            'Name': company_name,
            'Disclosure Date': disclosure_date,
            'Market Closed': True,
            'Reason': reason,
            'Opening Price': 'N/A',
            'Closing Price': 'N/A'
        })
        
        # Check subsequent days until the market reopens
        next_check_date = disclosure_date + datetime.timedelta(days=1)
        while True:
            next_open_date = utils_func.get_next_open_market_date(next_check_date)
            if next_open_date != disclosure_date:
                responses.append({
                    'Name': company_name,
                    'Disclosure Date': next_open_date,
                    'Market Closed': False,
                    'Reason': 'Market reopen',
                    'Opening Price': 'N/A',
                    'Closing Price': 'N/A'
                })
                break
            next_check_date += datetime.timedelta(days=1)

    if not responses:
        return None, False
    
    return responses, True

def fetch_and_process_stock_data(df_stock_data, company_id, disclosure_date, company_name):
    """
    Fetches and processes stock data for the given company and date.
    """
    stock_data = df_stock_data[(df_stock_data['CompanyID'] == company_id) & 
                               (df_stock_data['Date'] == disclosure_date)]
    if stock_data.empty:
        return {
            'Name': company_name,
            'Disclosure Date': disclosure_date,
            'Market Closed': False,
            'Reason': 'No stock data available',
            'Opening Price': 'N/A',
            'Closing Price': 'N/A'
        }

    opening_price = stock_data['Open'].iloc[0]
    closing_price = stock_data['Close'].iloc[0]
    return {
        'Name': company_name,
        'Disclosure Date': disclosure_date,
        'Market Closed': False,
        'Reason': '',
        'Opening Price': opening_price,
        'Closing Price': closing_price
    }

def process_company_data(row, df_stock_data):
    """
    Processes data for a single company based on disclosure date and available stock data.
    """
    disclosure_date = pd.to_datetime(row['Disclosure Date']).date()
    company_id = row['ID']
    company_name = row['Name']

    # Handle market closure scenarios
    market_closure_result, is_closed = handle_market_closure(disclosure_date, company_id, company_name)
    if is_closed:
        return market_closure_result

    # Handle regular stock data processing
    return fetch_and_process_stock_data(df_stock_data, company_id, disclosure_date, company_name)

def perform_analysis(df_disclosure_dates, df_stock_data):
    """
    Performs analysis by processing each company's data and compiles results into a DataFrame.
    """
    results = []
    for index, row in df_disclosure_dates.iterrows():
        result = process_company_data(row, df_stock_data)
        results.extend(result if isinstance(result, list) else [result])
    return pd.DataFrame(results)

def retrieve_data(query_function):
    """
    Retrieves data using the provided query function and handles exceptions.
    """
    try:
        data_frame = query_function()
        if data_frame is None or data_frame.empty:
            print("No data found or unable to retrieve data.")
            return pd.DataFrame()
        return data_frame
    except Exception as e:
        print("Error retrieving data:", e)
        return pd.DataFrame()

def run_stock_analysis():
    # Main function to orchestrate the retrieval and processing of stock data and its analysis.
    df_disclosure_dates = retrieve_data(db_functions.retrieve_company_disclosure_dates)
    df_stock_data = retrieve_data(db_functions.retrieve_stock_data)

    if df_disclosure_dates.empty or df_stock_data.empty:
        print("Data retrieval failed, skipping analysis.")
        return

    df_disclosure_analysis = perform_analysis(df_disclosure_dates, df_stock_data)
    output_file = "output\\analysis_workbook.xlsx"
    
    # Using ExcelWriter to save DataFrame to specific sheet
    with pd.ExcelWriter(output_file) as writer:
        df_disclosure_analysis.to_excel(writer, sheet_name='Disclosure Dates', index=False)
    
    print("Analysis data saved to Excel workbook.")