from craigslist import CraigslistForSale  # to get info from cl
from datetime import datetime  # to update the last query dt
import time  # to sleep btw the queries
import smtplib  # to send the email
from os import path  # to check if the log exists in the dir


def conv_date_time(dt):
    """Convert date time from str(%Y-%m-%d %H:%M)" to int(YmdHM)
       ex convert '2020-01-01 00:00' to 202001010000

    Args:
        dt (str): date time in %Y-%m-%d %H:%M format

    Returns:
        int: YearMonthDayHourMin
    """
    return int(dt.replace('-', '').replace(':', '').replace(' ', ''))


def isLaterDate(dt, dt_query):
    """Determine if the date is above the threshold date time

    Args:
        dt (str): date time in %Y-%m-%d %H:%M format
        dt_query (type): threshhold date time in %Y-%m-%d %H:%M format

    Returns:
        bool: True if above
    """
    if conv_date_time(dt) > conv_date_time(dt_query):
        return True
    return False


def results_msg(results_fresh, query_preod):
    """Generate a human readable summary of query results for query preod

    Args:
        results_fresh (List[dict()]): list of queries in dict format
        query_preod (str): dates and times of the query period

    Returns:
        str: The summary of query results
    """
    if not len(results_fresh):
        return ''
    msg = f'New results {query_preod}\n\n'
    for d in results_fresh:
        msg += f"{d['name']} {d['price']}\n{d['url']}\n\n"
    return msg + f"{20*'-'}"


def send_gmail(email_adr, psw, subj, msg):
    """Send an email to gmail with the query results

    Args:
        email_adr (str): gmail adress
        psw (str): password
        subj (str): subject of the email
        msg (str): mody of the email

    Returns:
        None
    """
    # gmail
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(email_adr, psw)
    server.sendmail(email_adr, email_adr, f'Subject: {subj}\n\n{msg}')


def init(begin_date_time, dt_file_name,query_res_file_name):
    """Initialize log and query time start

    Args:
        begin_date_time (str): date time of staring query in %Y-%m-%d %H:%M format
        dt_file_name (str): name of the file where dt of queries are saved
        query_res_file_name (str): name of the file where res of queries are saved

    Returns:
        None
    """
    # initialize the starting query date time
    if not path.exists(dt_file_name):
        with open(dt_file_name, 'w') as f:
            f.write(begin_date_time)

    # init log.txt if does not exist
    if not path.exists(query_res_file_name):
        f = open(query_res_file_name, "w")
        f.close()


# Craigslist query stuff
my_query = 'dresser'
min_price = 10
max_price = 50
begin_date_time = '2019-12-20 00:00'

# query times
sleep_time = 60*60*1 #secs
total_duration = 1*sleep_time

# Email info
email_adr = 'something@gmail.com'
psw = 'somepassword'


# init the starting query date time and log.txt if does not exist
dt_file_name = "last_query_dt.txt"
query_res_file_name = 'log.txt'
init(begin_date_time, dt_file_name,query_res_file_name)

duration = 0  # secs
while duration < total_duration:
    # query craigslist
    cl_sale = CraigslistForSale(site='santabarbara', category='sss',
                                filters={'query': my_query,
                                         'min_price': min_price,
                                         'max_price': max_price})
    # CraigslistForSale.show_filters()
    results = list(cl_sale.get_results(sort_by='newest'))

    # get the results since the last date time of the query
    dt_query = open(dt_file_name).read().strip()
    results_fresh = [d for d in results if isLaterDate(d['datetime'], dt_query)]

    # update the last date time of quering
    dt_query_new = datetime.now().strftime("%Y-%m-%d %H:%M")
    with open(dt_file_name, 'w') as f:
        f.write(dt_query_new)

    # save in human readable format if new query results are non empty
    query_period = dt_query + ' --> ' + dt_query_new
    msg = results_msg(results_fresh, query_period)
    if msg:
        # save the results to log
        with open(query_res_file_name, 'a') as f:
            f.write(msg)
        # email the results
        send_gmail(email_adr, psw, 'craigslist results', msg)

    duration += sleep_time
    time.sleep(sleep_time)
