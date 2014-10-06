#!/usr/bin/python3

import urllib.request, re

#requested = urllib.request.urlopen('http://uk-postcodes.com/postcode/NG92HF.csv')
#apicsv = requested.read()
# If you display csv you get:
#b'NG9 2HF,52.93003451787803,-1.2093035957311296,453247.0,337251.0,http://geohash.org/gcrjh7x7v1tf,E10000024,Nottinghamshire,E07000172,Broxtowe,E05006404,Beeston Central\n'
# comma separated data
#splitted = str(apicsv).split(',')
#requested.close()

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
    'MissaEF':'Mass (EF)',
    'MissaOF':'Mass (OF)',
    'MissamEF':'Mass (EF)',
    'MissamOF':'Mass (OF)',
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
    'Tenebrae':'Tenebrae',
    'tenebrae':'Tenebrae',
    'passio':'the Passion',
    'Passio':'the Passion',
    'PassioDomini':'the Passion',
    'passiodomini':'the Passion',
}

# Benedictine websites
class Monastery(object):
    def __init__(self, number, name, website, altname = None):
        self.number = number
        self.website = website
        self.name = name
        if altname:
            self.altname = altname
        else:
            self.altname = name

# regular expression that finds mp3 urls
mp3expression = """enclosure url=\\\*['"]http[^ ]*\.mp3"""
urlexpression = """enclosure url=\\\*['"](http[^ ]*\.mp3)"""
dateexpression = """([0-9]*)\.mp3"""
officeexpression = """/([a-zA-z]*?)_.*\.mp3"""

# instances of monasteries
norcia = Monastery(1, "Norcia", "http://osbnorcia.org/feed", "Nursia")
lebarroux = Monastery(2, "Le Barroux", "http://feeds.feedburner.com/RecordingLeBarroux")
vatican = Monastery(3, "Radio Vaticana", ("http://media01.vatiradio.va/podmaker/podcaster.aspx?c=vespri_lat", \
                                          "http://media01.vatiradio.va/podmaker/podcaster.aspx?c=compieta", \
                                          "http://media01.vatiradio.va/podmaker/podcaster.aspx?c=lodi"), "Vatican Radio")
                                 
requested = []           
fullfeed = ''                      
for i in range(len(vatican.website)):
    requested.append(urllib.request.urlopen(vatican.website[i]))
    fullfeed += str(requested[i].read())
    requested[i].close()

feedlist = re.findall(mp3expression, fullfeed)
mp3list = []
for mp3 in feedlist:
    url = re.findall(urlexpression, mp3)[0]
    dmy_date = re.findall(dateexpression, mp3)[0]
    dd = dmy_date[0:2]
    mm = dmy_date[2:4]
    yy = dmy_date[4:6]
    ymd_date = yy + mm + dd # turn day-month-year into year-month-day, will help with sorting below
    office = re.findall(officeexpression, mp3)[0]
    mp3list.append( (url, dmy_date, ymd_date, office) )

# sort the list by year-month-day date [2], reversed (starting with most recent date)
mp3list = sorted(mp3list, key=lambda x: x[2], reverse=True)

