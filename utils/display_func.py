# display_func.py

# Python Libraries
from datetime import datetime
import textwrap
from tabulate import tabulate

# Custom Libraries
from . import app_config

def print_centered_line(text="", padding=" ", border="**"):
    """Helper function to print a line with centered text and optional borders."""
    line_width = app_config.LINE_LENGTH - len(border) * 2 - 2  # Adjust for borders and padding
    formatted_text = f"{border:<2}{text:^{line_width}}{border:>2}"
    print(formatted_text)

def display_welcome_message():
    """Display a welcome message with the current date and time."""
    now = datetime.now()
    formatted_date_time = now.strftime("%B %d, %Y %I:%M %p")
    header = "*" * app_config.LINE_LENGTH
    
    print(f"\n{header}")
    print_centered_line(app_config.APP_TITLE)
    print_centered_line()  # Empty line for spacing
    print_centered_line(formatted_date_time)
    print(header)

def about_message():
    """Display information about the application."""
    description = (
        "This application aims to analyze publicly traded company's stock market data "
        "to determine if there is any correlation between database-related events and "
        "stock market prices. By exploring historical stock prices alongside "
        "database-related data, the goal is to gain insights into potential relationships "
        "and effects on stock market performance."
    )
    
    wrapped_description = textwrap.wrap(description, width=app_config.LINE_LENGTH - 4)  # Wrap text
    header = "*" * app_config.LINE_LENGTH

    print(header)
    print_centered_line("About")
    for line in wrapped_description:
        print_centered_line(line)
    print(header)

def display_compnay_info(company_info_df):
    if company_info_df.empty:
        print("[Error] No company information retrieved.")
    else:
        # Convert DataFrame to a list of lists without including the index
        company_info = company_info_df.values.tolist()
        headers = company_info_df.columns.tolist()

        # Display the company information in a nice table format without the index
        print("\nCompany Information:")
        print(tabulate(company_info, headers=headers, tablefmt="pretty"))

def display_polygon_header_key():
    """Displays a well-formatted header key for interpreting stock data."""
    print("\n" + "="*50)
    print("Stock Data Key Terms".center(50))
    print("="*50)
    
    # Display key definitions
    key_terms = [
        ("Date", "The date of the trading day."),
        ("Open", "Opening price of the stock."),
        ("Close", "Closing price of the stock."),
        ("High", "Highest price during the trading day."),
        ("Low", "Lowest price during the trading day."),
        ("Volume", "Total shares traded during the day."),
        ("VWAP", "Volume Weighted Average Price (A measure of the avg price).")
    ]
    
    # Print each term with its definition
    for term, description in key_terms:
        print(f" - {term:<10}: {description}")
    
    print("\n" + "="*50 + "\n")
