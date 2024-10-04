# main.py

import pandas as pd

from database import db_functions, db_check_stock_records
from utils import display_func, utils_func, app_config
from analysis import process_disclosure_dates
from tabulate import tabulate

def main_menu():
    """Display the main menu with 'Main Menu' as the title."""
    options = [
        "1. Company Information",
        "2. Data Breach Disclosure Dates",
        "3. Get Company Stock Data",
        "4. Check for Duplicate Stock Records",
        "5. Run Stock Analysis",
        "6. About",
        "7. Exit"
    ]

    print("\n" + "=" * app_config.LINE_LENGTH)
    print(f"{'Main Menu'.center(app_config.LINE_LENGTH)}")
    print("=" * app_config.LINE_LENGTH + "\n")
    print("Please select an option from the menu below:\n")
    
    for option in options:
        print(f"    {option}")
    
    print("\n" + "=" * app_config.LINE_LENGTH)

def handle_menu_choice(choice):
    """Handles the menu choice entered by the user."""
    if choice == "1":
        company_info_df = db_functions.retrieve_company_info()
        display_func.display_compnay_info(company_info_df)

        # Prompt user for saving to Excel
        utils_func.prompt_save_excel(company_info_df, "company_info.xlsx")

    elif choice == "2":
        disclosure_dates_df = db_functions.retrieve_company_disclosure_dates()
        if disclosure_dates_df.empty:
            print("[Error] No disclosure dates retrieved.")
        else:
            # Ensure the 'Disclosure Date' column is converted to datetime format
            disclosure_dates_df['Disclosure Date'] = pd.to_datetime(disclosure_dates_df['Disclosure Date'], errors='coerce')

            # Format the Disclosure Date to have abbreviated month names (e.g., 'Mar' instead of '03')
            disclosure_dates_df['Disclosure Date'] = disclosure_dates_df['Disclosure Date'].dt.strftime("%b %d, %Y")

            # Convert DataFrame to a list of lists without including the index
            disclosure_dates = disclosure_dates_df.values.tolist()
            headers = disclosure_dates_df.columns.tolist()

            # Display the disclosure dates in a nice table format without the index
            print("\nDisclosure Dates:")
            print(tabulate(disclosure_dates, headers=headers, tablefmt="pretty"))

            # Perform analysis - Number of disclosure dates per company and most recent disclosure
            analysis_df = disclosure_dates_df.groupby(['ID', 'Name', 'Symbol']).agg(
                num_disclosures=('Disclosure Date', 'count'),
                most_recent_disclosure=('Disclosure Date', 'max')
            ).reset_index()

            # Merge the analysis data with the original DataFrame for exporting
            merged_df = pd.merge(disclosure_dates_df, analysis_df, on=['ID', 'Name', 'Symbol'], how='left')

            # Rename columns for clarity
            merged_df = merged_df.rename(columns={
                'num_disclosures': '# Disclosures',
                'most_recent_disclosure': 'Most Recent'
            })

            # Display analysis results in the required format
            analysis_headers = ["ID", "Name", "Symbol", "# Disclosures", "Most Recent"]
            analysis_data = analysis_df.values.tolist()
            
            print("\nDisclosure Dates Analysis:")
            print(tabulate(analysis_data, headers=analysis_headers, tablefmt="pretty"))
            
            # Export the merged data (including the new columns) to an Excel file
            utils_func.output_to_excel(merged_df, "disclosure_dates_with_analysis.xlsx")
            print("Disclosure dates exported to 'disclosure_dates_with_analysis.xlsx'.")

    elif choice == "3":
        # Display Company Info
        company_info_df = db_functions.retrieve_company_info()
        display_func.display_compnay_info(company_info_df)

        # Prompt the user if they want to limit the results by specific company IDs
        limit_results = input("\nWould you like to limit the results by specific Company IDs? (y/n): ").strip().lower()
        
        company_ids = None
        if limit_results == "y":
            company_ids_input = input("Enter the Company IDs separated by commas (e.g., 1, 2, 3): ").strip()
            try:
                # Convert the input string to a list of integers (company IDs)
                company_ids = [int(company_id.strip()) for company_id in company_ids_input.split(',')]
            except ValueError:
                print("[Error] Invalid input. Please enter valid company IDs separated by commas.")
                return  # Exit the function to prevent further errors

        # Get Stock Data, passing the list of company IDs if available
        df_stock_data = db_functions.retrieve_stock_price_and_dow_jones_data(company_ids=company_ids)
        if df_stock_data is None or df_stock_data.empty:
            print("[Error] No stock data retrieved.")
        else:
            utils_func.output_to_excel(df_stock_data, "stock_price_and_dow_jones.xlsx")

    elif choice == "4":
        db_check_stock_records.check_for_duplicate_rows()

    elif choice == "5":
        process_disclosure_dates.run_stock_analysis()

    elif choice == "6":
        display_func.about_message()

    elif choice == "7":
        print("\nExiting the program. Have a nice day!")
        return False

    else:
        print("\n[Error] Invalid choice. Please select a valid option.")
    
    return True

def main():
    """Main function to run the application."""
    display_func.display_welcome_message()
    
    while True:
        main_menu()
        choice = input("\nEnter your choice: ").strip()
        if not handle_menu_choice(choice):
            break
        input("\nPress Enter to return to the main menu...")

if __name__ == "__main__":
    main()
