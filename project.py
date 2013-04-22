import xml.etree.ElementTree as ET
import urllib2 
import time
from datetime import date

file = urllib2.urlopen('http://domain.com/projects.rss?token=somehash')

data = file.read()
file.close()
exportName = 'projects.md'

root = ET.fromstring(data)

#def formatProject(item):
    #return item

priority = 1

now = date.today()
header = '# My projects as of %s\n\n' % now 
with open(exportName, 'w') as myfile:
    myfile.write(header)

for item in root.findall('channel/item'):
    title = item.find('title').text
    with open(exportName, "a") as myfile:
        number = "%i. " % (int(priority))
        myfile.write(number)
        myfile.write(title)
        myfile.write('\n')
    priority = priority + 1
