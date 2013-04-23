import xml.etree.ElementTree as ET
import urllib2 
import time
from datetime import date
import ConfigParser

# Get variables from the config file
config = ConfigParser.RawConfigParser()
config.read('project.conf')
projectsURL = config.get('General Information', 'projectsURL')
exportName = config.get('General Information', 'outputfile')

file = urllib2.urlopen(projectsURL)

data = file.read()
file.close()

root = ET.fromstring(data)



def createHeader():
    name = config.get('General Information', 'yourname')
    now = date.today()
    header = '# %s\'s projects as of %s\n\n' % (name,now)
    with open(exportName, 'w') as myfile:
        myfile.write(header)

def createProjectList(xml):
    priority = 1 # set the variable

    # Loop through xml object
    for item in root.findall('channel/item'):
        title = item.find('title').text
        with open(exportName, "a") as myfile:
            number = "%i. " % (int(priority))
            myfile.write(number)
            myfile.write(title)
            myfile.write('\n')
        priority = priority + 1


    print 'File should be saved, take a look at\n\n%s\n' % exportName

createHeader()
createProjectList(root)
