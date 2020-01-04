from craigslist import CraigslistForSale
from datetime import datetime
import time

def conv_date_time(dt):
    # ex convert '2020-01-01 00:00' to 202001010000
    return int(dt.replace('-', '').replace(':', '').replace(' ',''))

def isLaterDate(dt,dt_thresh):
    if conv_date_time(dt) > conv_date_time(dt_thresh):
        return True
    return False


# CraigslistForSale.show_filters()
my_query = 'dresser'
min_price = 10
max_price = 50

cl_sale = CraigslistForSale(site='santabarbara', category='sss',
                         filters={'query':my_query,
                                  'min_price':min_price,
                                  'max_price': max_price})
results =  list(cl_sale.get_results(sort_by='newest'))




dt_file_name = "craigslist_date.txt"
sleep_time = 60*60 #secs
thresh_duration = sleep_time*10
duration = 0 #secs
while duration < thresh_duration
    date_time_thresh = open(dt_file_name).read().strip() # 2020-01-01 00:00 "%Y-%m-%d %H:%M"

    results_fresh = [d for d in results if isLaterDate(d['datetime'],date_time_thresh)]
    #do stuff
    dt = datetime.now().strftime("%Y-%m-%d %H:%M")
    with open(dt_file_name, 'w') as f: f.write(dt)
    duration+=sleep_time
    time.sleep(sleep_time)
