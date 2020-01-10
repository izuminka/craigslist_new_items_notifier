# Overview
This is a simple email notifier for Craigslist's new items for sale. For
example if you are looking to purchase a dresser and you have looked at all items
on Craigslist under the query: dresser (in range $10-$50), this program will keep an eye
on new postings every couple of minute/hours. If something new appears under that query, the program
will send you all new postings to your gmail.

# Prerequisites
- **[Python 3](https://www.python.org/downloads/)**

- **Gmail account**
    - [Enable 2 step verification](https://www.google.com/landing/2step/),
    - [Generate App Password](https://myaccount.google.com)

- **[python-craigslist](https://pypi.org/project/python-craigslist)** - Craigslist wrapper

- **[APScheduler](https://pypi.org/project/APScheduler/2.1.2)** - Advanced Python Scheduler

       pip install python-craigslist
       pip install APScheduler=3.6.3


# Configuring

After installing the prerequisites open user_setup.json and enter information
related to the query:
- "gmail": your gmail address
- "gmail_psw": the generated password from https://myaccount.google.com
- "city": city/area you want to search (found https://city.craigslist.org/)
- "my_query": your Craigslist query
- "begin_date_time" :  ex: "2019-12-20 00:00"
- "min_price": min price for the item ex: 10
- "max_price": max price for the item ex: 10
- "hours": number of hours, ex: 1, 0.5, 0.003

Once the user_setup.json is done, open the terminal and type:

       python main.py


<!--
# Demo
![test demo](test.gif)
-->
