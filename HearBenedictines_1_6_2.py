#!/usr/bin/env python3

import urllib.request, re
from webbrowser import open as webbrowseropen

version = "Version 1.6.2, last updated Feast of St Martin, 2014."

def title():
    print("")
    print(" ###############################################################")
    print(" #/          +       /+\       \#/      /+\                   \#")
    print(' #          / \     """""       #      """""                   #')
    print(" #         / 0 \    | n |       #      |n n|                   #")
    print(" #      /\/: _ :\/\ | H |       #      |H H|                   #")
    print(' #      |/_:(@):_\|-"""""       #     /""""""""""""""""""      #')
    print(' #      ===========-|  0|       #    /|""""""""""""""""""      #')
    print(" #      |  ^/@\^  |\|   |       #   /H| |  H   H   H   H       #")
    print(" #                              #                              #")
    print(" #           HEAR THE           #           HEAR THE           #")
    print(" #    BENEDICTINES OF NURSIA    #  BENEDICTINES OF LE BARROUX  #")
    print(" #   SING THEIR DAILY OFFICES   #   SING THEIR DAILY OFFICES   #")
    print(" #                              #                              #")
    print(" #             [I]              #             [II]             #")
    print(" #\                            /#\                            /#")
    print(" ###############################################################")
    print(" #                                                             #")
    print(" #    HEAR THE LITURGY OF THE HOURS ON RADIO VATICANA [III]    #")
    print(" #                                                             #")
    print(" ###############################################################")
    print("")
    which_monast = input("                             [1/2/3]\n                             [Q]uit\n >")
    return which_monast

def loading():
    print(" Loading...")
    print("")

###################################################################################
###################################################################################

OFFICES = {
    'vespers':'Vespers',
    'vesperas':'Vespers',
    'completorium':'Compline',
    'matutinas':'Matins',
    'matutinum':'Matins',
    'primas':'Prime',
    'prima':'Prime',
    'laudes':'Lauds',
    'missa':'Mass',
    'missam':'Mass',
    'missaef':'Mass (EF)',
    'missaof':'Mass (OF)',
    'missamef':'Mass (EF)',
    'missamof':'Mass (OF)',
    'missam_of':'Mass (OF)',
    'missa_of':'Mass (OF)',
    'missam_ef':'Mass (EF)',
    'missa_ef':'Mass (EF)',
    'tertias':'Terce',
    'sextas':'Sexts',
    'nonas':'Nones',
    'vesper':'Vespers',
    'compline':'Compline',
    'matins':'Matins',
    'lauds':'Lauds',
    'prime':'Prime',
    'terce':'Terce',
    'sext':'Sexts',
    'sexts':'Sexts',
    'none':'Nones',
    'nones':'Nones',
    'tenebrae':'Tenebrae',
    'passio':'the Passion',
    'passiodomini':'the Passion',
    'vespri':'Vespers',
    'vespri_lat':'Vespers',
    'lodi':'Lauds',
    'compieta':'Compline',
    'completorii':'Compline',
    'vesperae':'Vespers',
    'laudum':'Lauds',
    'laudis':'Lauds',
}

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

MONTHS = {
    '01': 'January',
    '02': 'February',
    '03': 'March',
    '04': 'April',
    '05': 'May',
    '06': 'June',
    '07': 'July',
    '08': 'August',
    '09': 'September',
    '10': 'October',
    '11': 'November',
    '12': 'December',
}

# dictionary for HTML codes
HTML_CODES = {
    "&#8217;": "'",
    "\\\\xe2\\\\x80\\\\x9c": '"',
    "\\\\xe2\\\\x80\\\\x9d": '"',
    "\\\\xc3\\\\xbc": 'ue',
}

# a function that takes a string and replaces some HTML codes saved in it with a plaintext equivalent
def html_code_to_plain(s):
    for key, value in HTML_CODES.items():
        s = re.sub(key, value, s)
    return s

# a function for turning the publication date from the feed into a year-month-day date
def pubdate_into_ymddate(pubdate):
    # turns something like 'Mon, 02 Jun 2014 12:01:01 +02:00' into '20140602'
    year = re.findall('[a-zA-Z]{3}, [0-9]{2} [a-zA-Z]{3} ([0-9]{4})', pubdate)[0]
    month = re.findall('[a-zA-Z]{3}, [0-9]{2} ([a-zA-Z]{3}) [0-9]{4}', pubdate)[0]
    month = PUB_DATE_MONTHS[month]
    day = re.findall('[a-zA-Z]{3}, ([0-9]{2}) [a-zA-Z]{3} [0-9]{4}', pubdate)[0]
    return year + month + day

# this function checks whether you're connected to the internet or not
def check_connectivity(reference):
    try:
        urllib.request.urlopen(reference, timeout=1)
        return True
    except urllib.request.URLError:
        return False

def retry_connect():
    retry = input("Can't reach website. Check your internet connection. [R]etry? [M]ain menu?\n >")
    if retry.lower() == 'm':
        return 'MainMenu'


# Benedictine websites
class Monastery(object):
    def __init__(self, number, name, website, parser, standard_url, altname = None):
        self.number = number
        self.website = website
        self.name = name
        self.standard_url = standard_url #something to help check for errors in urls
        if altname:
            self.altname = altname
        else:
            self.altname = name
        self.parser = parser
        self.mp3list = None
        self.bloglist = None
    
    # This is the main function that goes and gets a list of mp3s and their info
    # from the relevant website
    def getmp3list(self):
        requested = []
        fullfeed = ''
        for i in range(len(self.website)):
            while not check_connectivity(self.website[i]):
                result_of_retry = retry_connect()
                if result_of_retry == 'MainMenu':
                    return 'MainMenu'
            requested.append(urllib.request.urlopen(self.website[i]))
            fullfeed += str(requested[i].read())
            requested[i].close()
        feedlist = re.findall(mp3expression, fullfeed) # gets all the <item>s from
                                                       # the fullfeed
        mp3list = []
        bloglist = []
        for mp3 in feedlist:
            parsedmp3 = parser(mp3, self) # parse out the details from the items,
                                          # each monastery has its own function
            if parsedmp3[4]: # is the Office field filled?
                mp3list.append(parsedmp3) # then add it to the mp3list
            else: bloglist.append(parsedmp3) # otherwise add it to the bloglist
        # sort the list by year-month-day date [1], reversed (starting with most
        # recent date):
        mp3list = sorted(mp3list, key=lambda x: x[1], reverse=True)
        bloglist = sorted(bloglist, key=lambda x: x[1], reverse=True)
        self.mp3list = mp3list
        self.bloglist = bloglist

# regular expressions that finds mp3 urls, dates, titles, and office names
mp3expression = """<item>.*?</item>"""
urlexpression = """enclosure url=\\\*['"](http[^ ]*\.mp3)"""
bloglinkexpression = """<link>(.*?)</link>"""
titleexpression = """<title>(.*?)</title>"""
pubdateexpression = """<pubDate>(.*?)</pubDate>"""

norciadateexpression = """([0-9]*)n\.mp3"""
norciaofficeexpression = """([a-zA-Z]*_?[a-zA-Z]*)[0-9]*[a-zA-Z]*n\.mp3"""
# http://osbnorcia.org/wp-content/audio/mass/Vesperas20140827n.mp3

lebarrouxdateexpression = """([0-9]{4}-[0-9]{2}-[0-9]{2})-.*\.mp3"""
lebarrouxofficeexpression = """-([a-zA-Z]*)\.mp3"""
# http://archive.org/download/le-barroux-1409163309/Le_Barroux_2014-08-27--19-45-01-compline.mp3

vaticandateexpression = """([0-9]*)\.mp3"""
vaticanofficeexpression = """/([a-zA-Z]+_?[a-zA-Z]*)_[0-9]*\.mp3"""
# http://media01.vatiradio.va/podcast/feed/vespri_lat_270814.mp3

###################################################################################################
# these functions get information from the url and return a list of tuples storing that information
def norcia_parser(url):
    try:
        ymd_date = re.findall(norciadateexpression, url)[0]
    except IndexError:
        ymd_date = None
    try:
        office = re.findall(norciaofficeexpression, url)[0]
    except IndexError:
        office = None
    return (ymd_date, office)

def lebarroux_parser(url):
    try:
        ymd_date = re.findall(lebarrouxdateexpression, url)[0]
        ymd_date = re.sub('-', '', ymd_date)
    except IndexError:
        ymd_date = None
    try:
        office = re.findall(lebarrouxofficeexpression, url)[0]
    except IndexError:
        office = None
    return (ymd_date, office)

def vatican_parser(url):
    try:
        dmy_date = re.findall(vaticandateexpression, url)[0]
        dd = dmy_date[0:2]
        mm = dmy_date[2:4]
        yy = dmy_date[4:6]
        ymd_date = '20' + yy + mm + dd # turn day-month-year into year-month-day, will help with sorting below
    except IndexError:
        ymd_date = None
    try:
        office = re.findall(vaticanofficeexpression, url)[0]
    except IndexError:
        office = None
    return (ymd_date, office)

###################################################################################################

def date_checker(url_date, pub_date): #THIS FUNCTION WILL COMPARE TWO DATES
                    #ONE IS THE DATE OBTAINED FROM THE URL
                    #THE OTHER IS THE PUB_DATE FROM THE FEED
                    #IF THE URL DATE IS NOT THE CORRECT LENGTH
                    #(SOMETIMES NORCIA URLS CONTAIN TYPOS)
                    #IT WILL COMPARE IT AGAINST THE OTHER DATE AND HOPEFULLY FIX IT
    index = len(url_date)
    for i in range(len(url_date)):
        if url_date[i] != pub_date[i]:
            index = i
            break
    front = url_date[:index]
    back = url_date[index+1:]
    result = front + back
    if len(result) == 8: return front, back, result # will return None if not published on the same day as url says

def url_checker(url, standard): #THIS FUNCTION WILL COMPARE A GIVEN URL TO
#A STANDARD URL AND CHECK FOR A TYPO (SOMETIMES NORCIA URLS CONTAIN TYPOS)
    index = len(standard) - 1
    add_one = 0
    for i in range(len(standard)):
        if url[i] != standard[i]:
            index = i
            add_one = 1
            break
    front = standard[:index]
    back = url[index+add_one:]
    result = front + back
    return front, back, result

def parser(mp3, monastery):
# This function returns tuples.
# Each tuple contains:
# 0: the URL for the mp3,
# 1: the date taken from the URL in the YYYYMMDD format,
# 2: the publication date from the RSS feed in long format (e.g. 'Sat, 16 Aug 2014 16:08:16 +0000'),
# 3: the title of the office taken from the URL,
# 4: the name of the office in English as filtered through the OFFICES dictionary (will become the same as the title if no office name is available)
    try:
        url = re.findall(urlexpression, mp3)[0]
        title = re.findall(titleexpression, mp3)[0]
        pub_date = re.findall(pubdateexpression, mp3)[0]
        ymd_date, office = monastery.parser(url) # each monastery has its own
                                    # function to parse details out of the url
        if not ymd_date: ymd_date = pubdate_into_ymddate(pub_date)
        if not office: office = title
        checked_date = date_checker(ymd_date, pubdate_into_ymddate(pub_date))
                                # this should fix some typos in the url dates
        if checked_date: # might return a None value if not published on the
                         # same date as the url says
            ymd_date = checked_date[2]
        try:
            office = OFFICES[office.lower()]
            textdate = re.sub('^0', '', ymd_date[6:]) + " " + MONTHS[ymd_date[4:6]] + " " + ymd_date[:4]
            office += ' for ' + textdate
        except KeyError: # the office field becomes the same as the title if
                         # it can't find the office in OFFICES dictionary
            office = title
        checked_url = url_checker(url, monastery.standard_url)
        if checked_url:
            url = checked_url[2]
    except IndexError: #if you get a blog post or some other
                       #<item> that doesn't contain an mp3 url
        url = re.findall(bloglinkexpression, mp3)[0] # then return an empty
                                                     # office field
        title = re.findall(titleexpression, mp3)[0]  # (this sometimes
                                                     # happens on norcia) 
        title = html_code_to_plain(title) # get rid of certain html codes in the title
        pub_date = re.findall(pubdateexpression, mp3)[0]
        ymd_date =  pubdate_into_ymddate(pub_date)
        office = ''
    return (url, ymd_date, pub_date, title, office)

def display_blogs(monastery):
    # A FUNCTION THAT DISPLAYS THE LIST OF BLOGS AND GETS THE USER TO CHOOSE ONE
    for i in range(len(monastery.bloglist)):
        print('[' + str(i + 1) + '] ' + monastery.bloglist[i][3])    
    blog_number = input('\n >')
    #check if a number has been entered:
    try:
        int(blog_number)
        while int(blog_number) < 1 and int(blog_number) > len(monastery.bloglist):
            blog_number = input('\n >')
        return blog_number
    #if it's not an integer
    except: pass

# the function that runs when a monastery is selected at the prompt
def choosechant(monastery):
    if not monastery.mp3list:
        anything_returned = monastery.getmp3list()
        if anything_returned: # returns 'MainMenu' if not connected to internet and don't want to retry
            return anything_returned
    # some display about how many mp3s/blogposts were found
    border = "#"
    mp3detectstring = " " + str(len(monastery.mp3list)) + " mp3s detected."
    if monastery.bloglist:
        blogdetectstring = " " + str(len(monastery.bloglist)) + " blog posts detected."
        maxdetectstring = max([len(mp3detectstring), len(blogdetectstring)])
    else: maxdetectstring = len(mp3detectstring)
    for i in range(maxdetectstring):
        border += "#"
    print(border)
    print(mp3detectstring)
    if monastery.bloglist: print(blogdetectstring)
    print(border)
    # asks the user what he wants to play
    # the loop breaks when something is played;
    # this if-structure informs user of blog posts
    if monastery.bloglist: blog_keypress = 'Or see [B]log posts? '
    else: blog_keypress = ''
    for i in range(len(monastery.mp3list)):
        print("")
        response = input(" Hear " + monastery.mp3list[i][4] + "? [Y/N] \n Or input the mp3's number? " + blog_keypress + "Or Main [M]enu?\n >")
        # 'tries' to turn response into an integer
        try:
            int(response)
        # if it gets an error (i.e. not an integer) it does this:
        except ValueError:
            response = response.lower()
            if response == "y":
                webbrowseropen(monastery.mp3list[i][0])
                break
            elif response == "m":
                break #breaks out of the mp3 choosing loop and goes back to main menu
            elif response == "b" and monastery.bloglist:
                result_from_display_blogs = display_blogs(monastery)
                if result_from_display_blogs:
                    blog_number = int(result_from_display_blogs) - 1
                    webbrowseropen(monastery.bloglist[blog_number][0])
                break
        # if it doesn't get an error (i.e. is an integer) it does this:
        else:
            if int(response) > 0 and int(response) <= len(monastery.mp3list):
                print("")
                response2 = input(" Hear " + monastery.mp3list[int(response)-1][4] + "? [Y/N] \n >")
                if response2 == "Y" or response2 == "y":
                    webbrowseropen(monastery.mp3list[int(response) - 1][0])
                    break
            else:
                print(" Sorry, that recording is not available!")

####################################################################################

# instances of Monasteries
norcia = Monastery(1, \
                   "Norcia", \
                   ["http://osbnorcia.org/feed"], \
                   norcia_parser, \
                   "http://osbnorcia.org/wp-content/audio/mass/", \
                   "Nursia")
lebarroux = Monastery(2, \
                      "Le Barroux", \
                      ["http://feeds.feedburner.com/RecordingLeBarroux"], \
                      lebarroux_parser, \
                      "http://archive.org/download/le-barroux-")
vatican = Monastery(3, \
                    "Radio Vaticana", \
                    ["http://media01.vatiradio.va/podmaker/podcaster.aspx?c=vespri_lat", \
                                          "http://media01.vatiradio.va/podmaker/podcaster.aspx?c=compieta", \
                                          "http://media01.vatiradio.va/podmaker/podcaster.aspx?c=lodi"], \
                    vatican_parser, \
                    "http://media01.vatiradio.va/podcast/feed/", \
                    "Vatican Radio")

# This dictionary will contain all the global Monastery class variables,
# with a key formatted for display, i.e., 'Liber Usualis'
#MONASTERIES = {}
#for monastery in [value for key, value in globals().items() if type(value).__name__ != 'classobj' and value.__class__.__name__ == "Monastery"]:
#    MONASTERIES[monastery.number] = monastery

# FOR TESTING:
# a function that lists the contents of one of the fields in a monastery list below
def testoffices(mp3list, n):
    for i in range(len(mp3list)):
        print(mp3list[i][n])

##################################################################################
# THE PROGRAM THAT RUNS:
# prints the title and gets an input:
# user chooses either Norcia ("1") or Le Barroux ("2") or Vatican ("3")
quit = None
while not quit:
    imp = title()
    while imp.lower() != "1" and imp != "2" and imp != "3" and imp != "i" and imp != "ii" and imp != "iii" and imp != "q":
        if imp.lower() == "v":
            imp = input(' ' + version + '\n\n >')
        else:
            imp = input(' Please choose [1] for Nursia, [2] for Le Barroux,\n [3] for Radio Vaticana or [V]ersion or [Q]uit. \n\n >')
    
    if imp == "Q" or imp == "q":
        break
    else:        
        # prints loading message
        loading()
            
    # puts choice into choosechant function
    if imp == "1" or imp == "i" or imp == "I":
        anything_returned = choosechant(norcia)
    elif imp == "2" or imp == "ii" or imp == "II":
        anything_returned = choosechant(lebarroux)
    else:
        anything_returned = choosechant(vatican)


