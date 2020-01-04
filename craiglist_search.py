from craigslist import CraigslistForSale

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

cl_h = CraigslistForSale(site='santabarbara', category='sss',
                         filters={'query':my_query,
                                  'min_price':min_price,
                                  'max_price': max_price})
results =  list(cl_h.get_results(sort_by='newest'))

date_time_thresh = '2020-01-01 00:00'
results_fresh = [d for d in results if isLaterDate(d['datetime'],date_time_thresh)]
