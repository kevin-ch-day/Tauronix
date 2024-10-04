import matplotlib.pyplot as plt
import os

# Plot Stock Prices (Closing, VWAP, Open, High, Low)
def plot_stock_data(company_name, dates, closing_prices, vwap=None, open_prices=None, high_prices=None, low_prices=None):
    plt.figure(figsize=(12, 6))

    # Plot Closing Prices
    plt.plot(dates, closing_prices, marker='o', label='Closing Price')

    # Plot VWAP if available
    if vwap:
        plt.plot(dates, vwap, marker='s', linestyle='-', label='VWAP')

    # Plot Open Prices if available
    if open_prices:
        plt.plot(dates, open_prices, marker='^', label='Open Price')

    # Plot High Prices if available
    if high_prices:
        plt.plot(dates, high_prices, marker='>', linestyle=':', label='High Price')

    # Plot Low Prices if available
    if low_prices:
        plt.plot(dates, low_prices, marker='<', linestyle='-.', label='Low Price')

    # Customize the plot
    plt.title(f'{company_name} Stock Prices Over Time')
    plt.xlabel('Date')
    plt.ylabel('Price ($)')
    plt.xticks(rotation=45)
    plt.grid(True)

    # Show the legend to differentiate between the lines
    plt.legend(loc='best')

    # Ensure everything fits without overlap
    plt.tight_layout()

    # Clean and truncate company name for the filename
    cleaned_company_name = company_name.replace('.', '').replace(',', '').replace(' ', '')[:10]
    output_path = f'output/{cleaned_company_name}_Stock_Price_Over_Time.png'
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path)

    plt.close()  # Close the plot after saving


# Plot Volume Over Time
def plot_volume(company_name, dates, volume):
    plt.figure(figsize=(12, 6))

    # Plot Volume
    plt.plot(dates, volume, marker='x', linestyle='--', label='Volume')

    # Customize the plot
    plt.title(f'{company_name} Volume Over Time')
    plt.xlabel('Date')
    plt.ylabel('Volume')
    plt.xticks(rotation=45)
    plt.grid(True)

    # Show the legend
    plt.legend(loc='best')

    # Ensure everything fits without overlap
    plt.tight_layout()

    # Clean and truncate company name for the filename
    cleaned_company_name = company_name.replace('.', '').replace(',', '').replace(' ', '')[:10]
    output_path = f'output/{cleaned_company_name}_Volume_Over_Time.png'
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path)

    plt.close()  # Close the plot after saving


# Plot Number of Trades Over Time
def plot_number_of_trades(company_name, dates, num_trades):
    plt.figure(figsize=(12, 6))

    # Plot Number of Trades
    plt.plot(dates, num_trades, marker='*', linestyle='-', label='Number of Trades')

    # Customize the plot
    plt.title(f'{company_name} Number of Trades Over Time')
    plt.xlabel('Date')
    plt.ylabel('Number of Trades')
    plt.xticks(rotation=45)
    plt.grid(True)

    # Show the legend
    plt.legend(loc='best')

    # Ensure everything fits without overlap
    plt.tight_layout()

    # Clean and truncate company name for the filename
    cleaned_company_name = company_name.replace('.', '').replace(',', '').replace(' ', '')[:10]
    output_path = f'output/{cleaned_company_name}_Number_of_Trades_Over_Time.png'
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path)

    plt.close()  # Close the plot after saving
