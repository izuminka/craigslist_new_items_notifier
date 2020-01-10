from datetime import datetime  # to update the last query dt
import time  # to sleep btw the queries
import smtplib  # to send the email
from os import path  # to check if the log exists in the dir
from apscheduler.schedulers.blocking import BlockingScheduler # for rep. queries
from craigslist import CraigslistForSale  # to get info from cl
import json  # to parse the setup.json


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


def one_total_query():
    """Main. Perform the full query"""

    # user params setup
    user_setup_fn = 'user_setup.json'
    with open(user_setup_fn) as f:
        setup = json.load(f)

    # init log.txt if does not exist
    query_res_fn = 'log.txt'
    if not path.exists(query_res_fn):
        f = open(query_res_fn, "w")
        f.close()

    # query craigslist
    # CraigslistForSale.show_filters() for additional filters
    cl_sale = CraigslistForSale(site='santabarbara', category='sss',
                                filters={'query': setup['my_query'],
                                         'min_price': setup['min_price'],
                                         'max_price': setup['max_price']})
    results = list(cl_sale.get_results(sort_by='newest'))

    # get the results since the last date time of the query
    dt_query = setup['begin_date_time']
    results_fresh = [d for d in results if isLaterDate(d['datetime'], dt_query)]

    # update the last date time of quering
    dt_query_new = datetime.now().strftime("%Y-%m-%d %H:%M")
    setup['begin_date_time'] = dt_query_new
    with open(user_setup_fn, 'w') as f:
        json.dump(setup,f)

    # save in human readable format if new query results are non empty
    query_period = dt_query + ' --> ' + dt_query_new
    msg = results_msg(results_fresh, query_period)
    if msg:
        # save the results to log
        with open(query_res_fn, 'a') as f:
            f.write(msg)
        # email the results
        send_gmail(setup['gmail'], setup['gmail_psw'], 'craigslist results', msg)
    print(query_period, 'finished')


if __name__ == '__main__':
    f = open('user_setup.json')
    setup = json.load(f)
    f.close()
    scheduler = BlockingScheduler()
    scheduler.add_job(one_total_query, 'interval', hours=setup['hours'])
    scheduler.start()
