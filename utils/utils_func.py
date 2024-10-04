import os
import datetime

def prompt_save_excel(data_df, file_name):
    save_excel = input("\nSave this data to an Excel file? (y/n): ").strip().lower()
    if save_excel == "y":
        output_to_excel(data_df, file_name)
        print(f"Data exported to '{file_name}'.")

def output_to_excel(dataframe, filename, output_dir="output"):
    try:
        # Ensure the output directory exists
        os.makedirs(output_dir, exist_ok=True)
        
        # Combine the output directory with the filename
        output_path = os.path.join(output_dir, filename)
        
        dataframe.to_excel(output_path, index=False)
        print(f"\nData saved to '{output_path}' successfully.")
    
    except Exception as e:
        print(f"\n[!!] Error saving data to '{output_path}':", e)

def is_market_closed(date):
    month = date.month
    reason = None
    
    # Check if the date falls on a weekend (Saturday or Sunday)
    if date.weekday() == 5:  
        return True, "Saturday"
    
    elif date.weekday() == 6:
        return True, "Sunday"
    
    # Check if the date is Memorial Day (May 31, 2021)
    elif date == datetime.date(2021, 5, 31):
        return True, "Memorial Day"
    
    return False, reason

def get_next_open_market_date(org_date):
    
    # Increment the date until a non-holiday, non-weekend day is found
    iteration_count = 0
    next_date = org_date
    market_closed, reason = is_market_closed(next_date)
    while market_closed:
        iteration_count += 1
        next_date += datetime.timedelta(days=1)
        
        if iteration_count == 7:
            print("\n[!!] Error: exceeded maximum iterations.")
            print("Exiting application.")
            exit()
        
        market_closed, reason = is_market_closed(next_date)
    
    return next_date