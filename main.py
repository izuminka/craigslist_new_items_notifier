from craigslist import CraigslistForSale
from datetime import datetime
import time

def conv_date_time(dt):
    # ex convert '2020-01-01 00:00' to 202001010000
    return int(dt.replace('-', '').replace(':', '').replace(' ',''))

def isLaterDate(dt,dt_query):
    if conv_date_time(dt) > conv_date_time(dt_query):
        return True
    return False

def results_msg(results_fresh, query_preod):
    if not len(results_fresh):
        return ''
    msg = f'New results {query_preod}\n\n'
    for d in results_fresh:
        msg+=f"{d['name']} {d['price']}\n{d['url']}\n\n"
    return msg+f"{20*'-'}"


# CraigslistForSale.show_filters()
my_query = 'dresser'
min_price = 10
max_price = 50

cl_sale = CraigslistForSale(site='santabarbara', category='sss',
                         filters={'query':my_query,
                                  'min_price':min_price,
                                  'max_price': max_price})
results =  list(cl_sale.get_results(sort_by='newest'))


query_res_file_name = 'log.txt'
dt_file_name = "last_query_dt.txt"
sleep_time = 1#60*60 #secs
thresh_duration = sleep_time*10
duration = 0 #secs
while duration < thresh_duration:
    #query the results since the last date time of the query
    dt_query = open(dt_file_name).read().strip() # '2020-01-01 00:00' "%Y-%m-%d %H:%M"
    results_fresh = [d for d in results if isLaterDate(d['datetime'],dt_query)]

    #update the last date time of quering
    dt_query_new = datetime.now().strftime("%Y-%m-%d %H:%M")
    with open(dt_file_name, 'w') as f: f.write(dt_query_new)

    #save in human readable format if new query results are non empty
    msg = results_msg(results_fresh, dt_query+'-->'+dt_query_new)
    if msg:
        # file_name = dt_query.replace(' ','_').replace(':','-') +'--'+dt_query_new.replace(' ','_').replace(':','-')
        with open(query_res_file_name, 'a') as f: f.write(msg)

    duration+=sleep_time
    time.sleep(sleep_time)
