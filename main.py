from craigslist import CraigslistForSale # to get info from cl
from datetime import datetime # to update the last query dt
import time # to sleep btw the queries
import smtplib # to send the email
from os import path #to check if the log exists in the dir

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

def send_email(email_adr, psw, subj, msg):
    #gmail
    server = smtplib.SMTP('smtp.gmail.com',587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(email, psw)
    server.sendmail(email,email,f'Subject: {subj}\n\n{msg}')

def init(dt_file_name, begin_date_time, query_res_file_name):
    #initialize the starting query date time
    with open(dt_file_name, 'w') as f: f.write(begin_date_time)

    #init log.txt if does not exist
    if not path.exists(query_res_file_name):
        f= open(query_res_file_name,"w")
        f.close()


# Craigslist query stuff
my_query = 'dresser'
min_price = 10
max_price = 50
begin_date_time = '2020-01-01 00:00'

# query times
sleep_time = 5#60*60 #secs
total_duration = sleep_time*10

# Save info
query_res_file_name = 'log.txt'
dt_file_name = "last_query_dt.txt"

#Email info
email_adr = 'something@gmail.com'
psw = 'somepassword'




#init the starting query date time and log.txt if does not exist
init(dt_file_name, begin_date_time, query_res_file_name)

duration = 0 #secs
while duration < total_duration:
    # query craigslist
    cl_sale = CraigslistForSale(site='santabarbara', category='sss',
                             filters={'query':my_query,
                                      'min_price':min_price,
                                      'max_price': max_price})
                                      # CraigslistForSale.show_filters()
    results =  list(cl_sale.get_results(sort_by='newest'))

    #query the results since the last date time of the query
    dt_query = open(dt_file_name).read().strip() # '2020-01-01 00:00' "%Y-%m-%d %H:%M"
    results_fresh = [d for d in results if isLaterDate(d['datetime'],dt_query)]

    #update the last date time of quering
    dt_query_new = datetime.now().strftime("%Y-%m-%d %H:%M")
    with open(dt_file_name, 'w') as f: f.write(dt_query_new)

    #save in human readable format if new query results are non empty
    query_period = dt_query+' --> '+dt_query_new
    msg = results_msg(results_fresh, query_period)
    if msg:
        # save the results to log
        with open(query_res_file_name, 'a') as f: f.write(msg)
        # email the results
        send_email(email_adr, psw, 'craigslist results', msg)

    duration+=sleep_time
    time.sleep(sleep_time)
