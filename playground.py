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
        
        # Try different selectors for pre-market price
        pre_market = soup.find('span', {'data-testid': 'qsp-pre-price'})
        if not pre_market:
            pre_market = soup.find('fin-streamer', {'data-field': 'preMarketPrice'})
        
        regular_price = soup.find('fin-streamer', {
            'class': 'livePrice',
            'data-symbol': 'SPY',
            'data-field': 'regularMarketPrice'
        })
        
        post_market = soup.find('fin-streamer', {
            'data-field': 'postMarketPrice',
            'data-symbol': 'SPY'
        })

        print('\033[K', end='')
        current_time = datetime.now().strftime('%H:%M:%S')
        print(f"[{current_time}]", end=' ')
        
        if pre_market and pre_market.text:
            print(f"Pre: ${pre_market.text.strip()}", end=' | ')
            
        print(f"Regular: ${regular_price.get('data-value') if regular_price else 'N/A'}", end='')
        
        if post_market:
            print(f" | Post: ${post_market.get('data-value')}", end='')
        
        print('\r', end='', flush=True)
        time.sleep(10)

except KeyboardInterrupt:
    print("\nStopped price tracking")
except Exception as e:
    print(f"\nAn error occurred: {e}")
    print("Response content:", response.text[:500])  # Print first 500 chars of response for debugging