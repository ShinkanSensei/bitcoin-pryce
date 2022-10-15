"""A script to get the current price of bitcoin.

To get the current price of bitcoin, this script scrapes coindesk's page 
containing the current bitcoin price. It then prints whether the price has 
gone up or down the last 5 minutes.

This script is intended to be run once every now and then and NOT indefinitely.
If you try to access the API too often,
you will risk your public IP being blocked by Cloudflare.
"""

import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from bs4 import BeautifulSoup
import time
from datetime import datetime
LAST_PRICE = '0'

while True:
    try:
        session = requests.Session()
        retry = Retry(connect=3, backoff_factor=0.5)
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        url = "https://www.coindesk.com/price/bitcoin/"
        req = session.get(url, timeout = 5)
        ans = req.content
        soup = BeautifulSoup(ans, "html.parser")
        
        # The specific elements for finding the btc price with coindesk
        div = soup.find('div', class_="Box-sc-1hpkeeg-0 hVNoEK")
        price = (div.find('span', class_="typography__StyledTypography-owin6q-0 kPwwwV").get_text())
        if price != LAST_PRICE:
            # Print the price, last change and timestamp after every update
            print(f'BTC price: ${price} '+ '↑'*(price>LAST_PRICE) + '↓'*(price<LAST_PRICE) + f' --- Last update: {datetime.utcnow().isoformat()}')       
            LAST_PRICE = price
        time.sleep(300) # Seems to update every 5-10 mintues. The time should be increased to prevent the public ip from being blocked by coindesk.

    except KeyboardInterrupt:
        print("Program stopped by user...")
        quit()