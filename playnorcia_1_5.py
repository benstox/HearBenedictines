import urllib2
import re
import webbrowser

version = "Version 1.5, last updated 24 March, 2014."

def title():
    print ""
    print " ###############################################################"
    print " #/          +       /+\       \#/      /+\                   \#"
    print ' #          / \     """""       #      """""                   #'
    print " #         / 0 \    | n |       #      |n n|                   #"
    print " #      /\/: _ :\/\ | H |       #      |H H|                   #"
    print ' #      |/_:(@):_\|-"""""       #     /""""""""""""""""""      #'
    print ' #      ===========-|  0|       #    /|""""""""""""""""""      #'
    print " #      |  ^/@\^  |\|   |       #   /H| |  H   H   H   H       #"
    print " #                              #                              #"
    print " #           HEAR THE           #           HEAR THE           #"
    print " #    BENEDICTINES OF NURSIA    #  BENEDICTINES OF LE BARROUX  #"
    print " #   SING THEIR DAILY OFFICES   #   SING THEIR DAILY OFFICES   #"
    print " #                              #                              #"
    print " #             [I]              #             [II]             #"
    print " #\                            /#\                            /#"
    print " ###############################################################"
    print ""
    which_monast = raw_input("                              [1/2]\n                              [Q]uit\n\n >")
    return which_monast

def loading():
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
    'Matutinum':'Matins',
    'Primas':'Prime',
    'Prima':'Prime',
    'Laudes':'Lauds',
    'Missa':'Mass',
    'Missam':'Mass',
    'Tertias':'Terce',
    'Sextas':'Sexts',
    'Nonas':'Nones',
    'vespers':'Vespers',
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

# function to process the names of mp3s that are lectures
def getlecturename(mp3name):
    # it will go here if there are no numbers
    # i.e. there is no date in the name
    # e.g. sometimes they post lectures like 'FrCassianFolsom-Summorum_Pontificum_and_Liturgical_Law.mp3'
    #                                     or 'FrCassianFolsom-07_The_Eucharistic_Prayer.mp3'
    # '.mp3' should already be removed so:
    mp3name = re.sub('_', ' ', mp3name) # replaces underscores with spaces
    mp3name = re.sub('-', ' - ', mp3name) # replaces '-' with ' - '
    mp3name = re.sub(' 0+', ' ', mp3name) # replaces ' 0+' with ' ' to get rid of possible initial 0s
    mp3name = re.sub('([0-9]+)', 'Lecture \\1:', mp3name) # replaces numbers with 'Lecture ##:'
    mp3name = re.sub(' {2,}', ' ', mp3name) # gets rid of double (or more) spaces possibly caused by something above
    mp3name = re.sub('([a-z])([A-Z])', '\\1 \\2', mp3name) # adds a space between a lowercase followed by an uppercase
    return mp3name # would return 'Fr Cassian Folsom - Summorum Pontificum and Liturgical Law'
                   #           or 'FrCassianFolsom - Lecture 7: The Eucharistic Prayer'
    
# converts the output of a getmp3name()
# into the format of 'Vespers for 8 December 2013' or suchlike
def getofficenamedate(mp3name):
    #print mp3name
    mp3name = mp3name[:-4]
    # this should sort out Le Barroux mp3s
    if re.search('Barroux', mp3name):
        sansbarroux = re.search('[0-9].*', mp3name)
        mp3name = sansbarroux.group()
        numbers = re.search('([0-9]*)-([0-9]*)-([0-9]*)', mp3name)
        year = numbers.group(1)
        month = numbers.group(2)
        day = int(numbers.group(3))
        officename = re.search('[A-Za-z].*', mp3name)
        try:
            name = OFFICES[officename.group()]
        except KeyError:
            return "Office/Mass name not found in dictionary!"
            
    # this should sort out Norcia mp3s
    else:
        numbers = re.search('[0-9]+', mp3name)
        if numbers:
        # it will go here if there are any numbers in the name
        # i.e. if there is a date in the name
            rawdate = numbers.group()
            if len(rawdate) != 8:
                #return "ERROR!"
                #it will go here if there is a number but it doesn't appear to be a date (8 digits long)
                #e.g. sometimes they post lectures like 'FrCassianFolsom-07_The_Eucharistic_Prayer.mp3'
                return getlecturename(mp3name)
            year = rawdate[:4]
            month = rawdate[4:6]
            day = int(rawdate[6:])
            try:
                name = OFFICES[mp3name[:numbers.start()]]
            except KeyError:
                return "Office/Mass name not found in dictionary!"
        else:
            # it will go here if there are no numbers
            # i.e. there is no date in the name
            # e.g. sometimes they post lectures like 'FrCassianFolsom-Summorum_Pontificum_and_Liturgical_Law.mp3'
            return getlecturename(mp3name)
    date = str(day) + " " + MONTHS[month] + " " + year
    namedate = name + " for " + date
    return namedate
    
# Benedictine websites
class Monastery:
    def __init__(self, number, name, website, altname = None):
        self.number = number
        self.website = website
        self.name = name
        if altname:
            self.altname = altname
        else:
            self.altname = name

# instances of monasteries
norcia = Monastery(1, "Norcia", "http://osbnorcia.org/feed", "Nursia")
lebarroux = Monastery(2, "Le Barroux", "http://feeds.feedburner.com/RecordingLeBarroux")

# regular expression that finds mp3 urls
#expression = "http.*mp3"
#expression = "(http.*mp3)"
expression = 'enclosure url="http[^ ]*\.mp3'

def choosechant(choice):	
    global expression
    
    # gets the text of the feed website as a weird object
    text = urllib2.urlopen(choice.website)
    
    linelist = []
    mp3list = []

    # makes a list called linelist
    # each item in the list is a line of text from the site
    # it also makes a list called mp3list
    # and it checks each item in linelist for a url
    # it then adds the urls to mp3list
    for line in text:
        linelist.append(line)
        if re.search(expression, line):
            result = re.findall(expression, line)
            for i in range(len(result)):
                result[i] = re.sub('enclosure url="', '', result[i])
                mp3list.append(result[i])
    
    # just formats the ###s to fit nicely around the text
    #OLD METHOD:
    #digits = len(str(len(linelist)))
    #border = "##############################################"
    border = "#"
    textlinestring = " " + str(len(linelist)) + " lines of text at " + choice.website + "."
    mp3detectstring = " " + str(len(mp3list)) + " mp3s detected."
    for i in range(len(textlinestring)):
        border += "#"
    print border
    print textlinestring
    print mp3detectstring
    print border
    
    # asks the user what he wants to play
    # the loop breaks when something is played
    for i in range(len(mp3list)):
        mp3name = getmp3name(i, mp3list)
        print ""
        response = raw_input(" Hear " + getofficenamedate(mp3name) + "? [Y/N] \n Or input the mp3's number? Or Main [M]enu?\n >")
        # 'tries' to turn response into an integer
        try:
            int(response)
        # if it gets an error (i.e. not an integer) it does this:
        except ValueError:
            if response == "Y" or response == "y":
                webbrowser.open(mp3list[i])
                break
            elif response == "M" or response == "m":
                break #breaks out of the mp3 choosing loop and goes back to main menu
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

# prints the title and gets an input:
# user chooses either Norcia ("1") or Le Barroux ("2")
quit = None
while not quit:
    imp = title()
    while imp != "1" and imp != "2" and imp != "I" and imp != "II" and imp != "i" and imp != "ii" and imp != "Q" and imp != "q":
        if imp == "v" or imp == "V":
            imp = raw_input(' ' + version + '\n\n >')
        else:
            imp = raw_input(' Please choose [1] for Nursia or [2] for Le Barroux,\n or [V]ersion or [Q]uit. \n\n >')
    
    if imp == "Q" or imp == "q":
        break
    else:        
        # prints loading message
        loading()
            
    # puts choice into choosechant function
    if imp == "1" or imp == "i" or imp == "I":
        choosechant(norcia)
    else:
        choosechant(lebarroux)

    

