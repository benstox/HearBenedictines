#!/usr/bin/env python3

import re

PUB_DATE_MONTHS = {
    'Jan':'01',
    'Feb':'02',
    'Mar':'03',
    'Apr':'04',
    'May':'05',
    'Jun':'06',
    'Jul':'07',
    'Aug':'08',
    'Sep':'09',
    'Oct':'10',
    'Nov':'11',
    'Dec':'12',
}

# a function for turning the publication date from the feed into a year-month-day date
def pubdate_into_ymddate(pubdate):
    # turns something like 'Mon, 02 Jun 2014 12:01:01 +02:00' into '20140602'
    year = re.findall('[a-zA-Z]{3}, [0-9]{2} [a-zA-Z]{3} ([0-9]{4})', pubdate)[0]
    month = re.findall('[a-zA-Z]{3}, [0-9]{2} ([a-zA-Z]{3}) [0-9]{4}', pubdate)[0]
    month = PUB_DATE_MONTHS[month]
    day = re.findall('[a-zA-Z]{3}, ([0-9]{2}) [a-zA-Z]{3} [0-9]{4}', pubdate)[0]
    return year + month + day

def date_checker(url_date, pub_date): #THIS FUNCTION WILL COMPARE TWO DATES
                    #ONE IS THE DATE OBTAINED FROM THE URL
                    #THE OTHER IS THE PUB_DATE FROM THE FEED
                    #IF THE URL DATE IS NOT THE CORRECT LENGTH (SOMETIMES NORCIA URLS CONTAIN TYPOS)
                    #IT WILL COMPARE IT AGAINST THE OTHER DATE AND HOPEFULLY FIX IT
    index = len(url_date)
    for i in range(len(url_date)):
        if url_date[i] != pub_date[i]:
            index = i
            break
    front = url_date[:index]
    back = url_date[index+1:]
    result = front + back
    if len(result) == 8: return front, back, result
    #return front, back, result

url_date = '201400903'
pub_date = '20140903'

url_date_2 = '201401002'
pub_date_2_long = 'Thu, 02 Oct 2014 06:45:30 +0000'
pub_date_2 = pubdate_into_ymddate(pub_date_2_long)

date_checker(url_date, pub_date)
date_checker(url_date_2, pub_date_2)
date_checker('12345678', '12345678')


