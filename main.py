import requests
from bs4 import BeautifulSoup

def get_price(soup,html_price_id):
    price = soup.find(id=html_price_id).get_text()
    return float(price[price.find('$')+1:]) # strip and convert the price to float

def get_soup(url):
    page = requests.get(url) #leaving out headers
    return BeautifulSoup(page.content, 'html.parser')


EBAY_PRICE_ID = 'prcIsum_bidPrice'

URL = "https://www.ebay.com/itm/Signal-Disruptor-Snowboard-158-2018-Black-White-Yellow-With-Stomp-Pad/324026560704?hash=item4b717cf0c0%3Ag%3AHtgAAOSw08deCNCY&LH_Auction=1"
soup = get_soup(URL)

price = get_price(soup,EBAY_PRICE_ID)


# price_thresh = 200
# if price > price_thresh:
#     print(True)
