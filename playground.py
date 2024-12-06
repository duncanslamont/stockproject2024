from bs4 import BeautifulSoup
import requests
import time
from datetime import datetime

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

url = 'https://finance.yahoo.com/quote/SPY'

try:
    while True:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Get regular market price
        regular_price = soup.find('fin-streamer', {
            'class': 'livePrice',
            'data-symbol': 'SPY',
            'data-field': 'regularMarketPrice'
        })

        # Get post-market price
        post_market = soup.find('fin-streamer', {
            'data-field': 'postMarketPrice',
            'data-symbol': 'SPY'
        })

        # Clear previous line (optional - makes output cleaner)
        print('\033[K', end='')
        
        # Print current time and prices
        current_time = datetime.now().strftime('%H:%M:%S')
        print(f"[{current_time}] Regular: ${regular_price.get('data-value') if regular_price else 'N/A'}", end='')
        
        if post_market:
            print(f" | Post: ${post_market.get('data-value')}", end='')
        
        print('\r', end='', flush=True)  # Return cursor to start of line
        
        time.sleep(5)  # Wait for 5 seconds

except KeyboardInterrupt:
    print("\nStopped price tracking")