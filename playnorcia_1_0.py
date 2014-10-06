import urllib2
import re
import webbrowser

print "Loading..."
print ""

def getmp3name(x, urllist):
    lastpart = "/[^/]*\.mp3$"
    mp3name = re.search(lastpart, urllist[x])
    firstchar = mp3name.start() + 1
    lastchar = len(urllist[x])
    mp3name = urllist[x][int(firstchar):int(lastchar)]
    return mp3name

website = "http://osbnorcia.org/feed"
	
text = urllib2.urlopen(website)

linelist = []
mp3list = []

expression = "(http.*mp3)"

for line in text:
    linelist.append(line)
    if re.search(expression, line):
        result = re.search(expression, line)
        mp3list.append(result.group(1))

digits = len(str(len(linelist)))
border = "##############################################"
for i in range(digits):
    border += "#"
print border
print " " + str(len(linelist)) + " lines of text at http://osbnorcia.org/feed."
print " " + str(len(mp3list)) + " mp3s detected."
print border
print ""

for i in range(len(mp3list)):
    mp3name = getmp3name(i, mp3list)
    response = raw_input(" Play '" + mp3name + "'? [Y/N] \n Or input the mp3's number? \n ")
    try:
        int(response)
    except ValueError:
        if response == "Y" or response == "y":
            webbrowser.open(mp3list[i])
            break
    else:
        mp3name = getmp3name(int(response) - 1, mp3list)
        response2 = raw_input(" Play '" + mp3name + "'? [Y/N] \n ")
        if response2 == "Y" or response2 == "y":
            webbrowser.open(mp3list[int(response) - 1])
            break