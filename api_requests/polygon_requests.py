# Python Libraries
import requests
import time

# Custom Libraries
from database import db_functions

# Constants
BASE_URL = 'https://api.polygon.io'
RETRY_STATUS_CODES = [429, 503]  # Status codes that trigger a retry
MAX_RETRIES = 3  # Number of retry attempts
RETRY_WAIT_SECONDS = 5  # Wait time between retries in seconds

# Function to build the Polygon API URL
def build_request_url(ticker, from_date, to_date, multiplier=1, timespan='day'):
    """Builds the API request URL for Polygon API."""
    API_KEY = db_functions.get_polygon_api_key()
    return f"{BASE_URL}/v2/aggs/ticker/{ticker}/range/{multiplier}/{timespan}/{from_date}/{to_date}?adjusted=true&sort=asc&limit=120&apiKey={API_KEY}"

# Function to handle error responses from the API
def handle_error(response):
    """Handles API errors based on status codes."""
    status_code = response.status_code

    if status_code == 400:
        print(f"Bad Request (400): Invalid parameters provided. Please check your inputs.")
    elif status_code == 401:
        print(f"Unauthorized (401): Invalid API key or missing authentication.")
    elif status_code == 403:
        print(f"Forbidden (403): Access to the resource is denied. Check your API key permissions.")
    elif status_code == 404:
        print(f"Not Found (404): The requested resource could not be found. Check the ticker symbol or endpoint.")
    elif status_code == 429:
        print(f"Too Many Requests (429): Rate limit exceeded. Please try again later.")
    elif status_code == 500:
        print(f"Internal Server Error (500): The server encountered an error. Try again later.")
    elif status_code == 503:
        print(f"Service Unavailable (503): The service is temporarily unavailable. Please try again later.")
    else:
        print(f"Unexpected Error ({status_code}): {response.text}")

# Function to fetch aggregate data from Polygon API
def get_api_data(ticker, from_date, to_date, multiplier=1, timespan='day'):
    """Fetches stock data from the Polygon API with retry mechanism for certain errors."""
    url = build_request_url(ticker, from_date, to_date, multiplier, timespan)
    retries = 0

    while retries <= MAX_RETRIES:
        response = requests.get(url)

        # Handle successful response
        if response.status_code == 200:
            return response.json()  # Return the API response in JSON format

        # Handle specific response codes
        if response.status_code in RETRY_STATUS_CODES:
            # Retry for rate limit or service unavailable errors
            print(f"Error {response.status_code}: Retrying in {RETRY_WAIT_SECONDS} seconds...")
            time.sleep(RETRY_WAIT_SECONDS)
            retries += 1
        else:
            # For other errors, handle them and break
            handle_error(response)
            break

    print(f"Max retries reached. Failed to fetch data for {ticker}.")
    return None