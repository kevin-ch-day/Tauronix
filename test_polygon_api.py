# test_polygon_api.py

# Python Libraries
from datetime import datetime, timedelta

# Custom Libraries
from database import db_functions
from utils import utils_plots, display_func
from api_requests import polygon_requests

def process_stock_data(data):
    # Initialize total statistics
    total_open, total_close, total_volume = 0, 0, 0
    count = len(data['results'])

    # Initialize lists to store values
    dates, closing_prices, open_prices, high_prices, low_prices, volumes, vwaps, num_trades = [], [], [], [], [], [], [], []

    # Iterate through the stock data
    for result in data['results']:
        date = datetime.fromtimestamp(result['t'] / 1000).strftime('%Y-%m-%d')
        open_price = result['o']  # Get the opening price
        close_price = result['c']  # Get the closing price
        high_price = result['h']  # Get the highest price
        low_price = result['l']  # Get the lowest price
        volume = result['v']  # Get the volume
        vwap = result['vw']  # Get the VWAP
        trades = result['n'] # Get number of trades

        # Accumulate totals for summary statistics
        total_open += open_price
        total_close += close_price
        total_volume += volume

        # Append data to lists for plotting
        dates.append(date)
        closing_prices.append(close_price)
        open_prices.append(open_price)
        high_prices.append(high_price)
        low_prices.append(low_price)
        volumes.append(volume)
        vwaps.append(vwap)
        num_trades.append(trades)

    # Return the processed data as a dictionary
    return {
        'dates': dates,
        'closing_prices': closing_prices,
        'opening_prices': open_prices,
        'stock_highs': high_prices,
        'stock_lows': low_prices,
        'volume': volumes,
        'vwaps': vwaps,
        'stock_trades': num_trades,
        'total_open': total_open,
        'total_close': total_close,
        'total_volume': total_volume,
        'count': count
    }

# Function to format and display the API response data
def format_response(data):
    if data is None or 'results' not in data:
        print("\n[Error] No data to display. Please check your inputs.\n")
        return

    print("\n" + "="*60)
    print("Stock Data Summary".center(60))
    print("="*60)

    print(f"Ticker: {data['ticker']}")
    print(f"Query Count: {data['queryCount']}")
    print(f"Results Count: {data['resultsCount']}")
    print(f"Adjusted: {data['adjusted']}\n")

    display_func.display_polygon_header_key()

    # Process stock data using the new function
    stock_data = process_stock_data(data)

    # Print table header
    print(f"{'Date':<15} {'Open':<10} {'Close':<10} {'High':<10} {'Low':<10} {'Volume':<15} {'VWAP':<10}")

    # Loop through the processed data and display it
    for i in range(stock_data['count']):
        print(f"{stock_data['dates'][i]:<15} {stock_data['opening_prices'][i]:<10} {stock_data['closing_prices'][i]:<10} "
              f"{stock_data['stock_highs'][i]:<10} {stock_data['stock_lows'][i]:<10} {stock_data['volume'][i]:<15} "
              f"{stock_data['vwaps'][i]:<10}")

    # Display summary statistics
    print("\n" + "="*60)
    print("Summary Statistics".center(60))
    print("="*60)
    print(f"Average Open Price: {stock_data['total_open'] / stock_data['count']:.2f}")
    print(f"Average Close Price: {stock_data['total_close'] / stock_data['count']:.2f}")
    print(f"Total Volume Traded: {stock_data['total_volume']}")


# Main menu for the application
def display_menu():
    print("\n" + "="*60)
    print("Main Menu".center(60))
    print("="*60)
    print("1. Fetch Stock Data")
    print("2. Plot Stock Data")
    print("0. Exit")
    print("="*60)

# Function to get stock data and format it
def fetch_stock_data():
    while True:
        ticker = input("\nEnter the stock ticker symbol: ").strip().upper()
        if not ticker:
            print("\nNo value entered for stock ticker symbol (Example: VZ)")
            print("Please enter a value or '-1' to go back to the main menu.")
        elif ticker == "-1":
            return None
        else:
            break

    today = datetime.now()
    end_date = today.strftime('%Y-%m-%d')

    # Set start date 14 days ago to handle market closure (weekends or holidays)
    start_date = (today - timedelta(days=14)).strftime('%Y-%m-%d')

    from_date = input(f"Enter the start date (YYYY-MM-DD) [default: {start_date}]: ").strip() or start_date
    to_date = input(f"Enter the end date (YYYY-MM-DD) [default: {end_date}]: ").strip() or end_date

    # Fetch and format aggregate data
    aggregate_data = polygon_requests.get_api_data(ticker, from_date, to_date)

    results = db_functions.get_company_id_and_name_by_symbol(ticker)

    company_id = results['CompanyID']
    company_name = results['CompanyName']

    return aggregate_data, company_id, company_name

# Main application logic
def main():
    while True:
        display_menu()
        choice = input("Select an option: ").strip()

        if choice == '1':
            aggregate_data, company_id, company_name = fetch_stock_data()
            if aggregate_data:
                format_response(aggregate_data)

        elif choice == '2':
            aggregate_data, company_id, company_name = fetch_stock_data()

            if aggregate_data and 'results' in aggregate_data:
                
                # Process the stock data using the new function
                stock_data = process_stock_data(aggregate_data)
                
                # Ask the user if they want to plot the data and save it
                save_plots = input(f"\nDo you want to plot the data and save it? (y/n): ").strip().lower()
                if save_plots == 'y':
                    plot_stock_data(company_name, stock_data) 

        elif choice == '0':
            print("\nExiting the program.")
            break

        else:
            print("\n[Error] Invalid choice. Please select a valid option.")

def plot_stock_data(company_name, stock_data):
    # Clean the company name by removing any '.' or ',' and truncating to 10 characters
    cleaned_company_name = company_name.replace('.', '').replace(',', '').replace(' ', '')[:10]

    # Try plotting and saving the stock data and other metrics
    try:
        # Plot stock prices (closing, vwaps, open, high, low)
        utils_plots.plot_stock_data(cleaned_company_name,
                                    stock_data['dates'],
                                    stock_data['closing_prices'],
                                    stock_data['vwaps'],
                                    stock_data['opening_prices'],
                                    stock_data['stock_highs'],
                                    stock_data['stock_lows'])

        # Plot the number of trades
        utils_plots.plot_number_of_trades(cleaned_company_name,
                                          stock_data['dates'],
                                          stock_data['stock_trades'])

        # Plot the volume over time
        utils_plots.plot_volume(cleaned_company_name,
                                stock_data['dates'],
                                stock_data['volume'])

        # If no errors, display success message with cleaned and truncated company name
        print(f"\nPlots were saved as '{cleaned_company_name}_*.png' in the 'output' directory.")

    except Exception as e:
        print(f"\n[Error] An error occurred while plotting data: {e}")

# Run the script
if __name__ == '__main__':
    main()
