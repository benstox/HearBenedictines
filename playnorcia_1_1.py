import urllib2
import re
import webbrowser

print "##########################################################"
print ""
print " HEAR THE BENEDICTINES OF NURSIA SING THEIR DAILY OFFICES"
print ""
print "##########################################################"
print ""
print " Loading..."
print ""

# gets the mp3 filename from the end of a url
def getmp3name(x, urllist):
    lastpart = "/[^/]*\.mp3$"
    match = re.search(lastpart, urllist[x])
    firstchar = match.start() + 1
    mp3name = urllist[x][firstchar:]
    return mp3name
    
OFFICES = {
    'Vespers':'Vespers',
    'Vesperas':'Vespers',
    'Completorium':'Compline',
    'Matutinas':'Matins',
    'Primas':'Prime',
    'Prima':'Prime',
    'Laudes':'Lauds',
    'Missa':'Mass',
    'Tertias':'Terce',
    'Sextas':'Sexts',
    'Nonas':'Nones',
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
    '12': 'December'
}
    
def getofficenamedate(mp3name):
    mp3name = mp3name[:-4]
    numbers = re.search('[0-9]+', mp3name)
    rawdate = numbers.group()
    if len(rawdate) != 8:
        return "ERROR!"
    year = rawdate[:4]
    month = rawdate[4:6]
    day = rawdate[6:]
    date = day + " " + MONTHS[month] + " " + year
    name = OFFICES[mp3name[:numbers.start()]]
    namedate = name + " for " + date
    return namedate

# Benedictine website
website = "http://osbnorcia.org/feed"
	
# gets the text of the feed website as a weird object
text = urllib2.urlopen(website)

linelist = []
mp3list = []

# regular expression that finds urls
expression = "(http.*mp3)"

# makes a list called linelist
# each item in the list is a line of text from the site
# it also makes a list called mp3list
# and it checks each item in linelist for a url
# it then adds the urls to mp3list
for line in text:
    linelist.append(line)
    if re.search(expression, line):
        result = re.search(expression, line)
        mp3list.append(result.group(1))

# just formats the ###s to fit nicely around the text
digits = len(str(len(linelist)))
border = "##############################################"
for i in range(digits):
    border += "#"
print border
print " " + str(len(linelist)) + " lines of text at http://osbnorcia.org/feed."
print " " + str(len(mp3list)) + " mp3s detected."
print border

# asks the user what he wants to play
# the loop breaks when something is played
for i in range(len(mp3list)):
    mp3name = getmp3name(i, mp3list)
    print ""
    response = raw_input(" Hear " + getofficenamedate(mp3name) + "? [Y/N] \n Or input the mp3's number? \n >")
    # 'tries' to turn response into an integer
    try:
        int(response)
    # if it gets an error (i.e. not an integer) it does this:
    except ValueError:
        if response == "Y" or response == "y":
            webbrowser.open(mp3list[i])
            break
    # if it doesn't get an error (i.e. is an integer) it does this:
    else:
        if int(response) > 0 and int(response) <= len(mp3list):
            mp3name = getmp3name(int(response) - 1, mp3list)
            print ""
            response2 = raw_input(" Hear " + getofficenamedate(mp3name) + "? [Y/N] \n >")
            if response2 == "Y" or response2 == "y":
                webbrowser.open(mp3list[int(response) - 1])
                break
        else:
            print " Sorry, that recording is not available!"