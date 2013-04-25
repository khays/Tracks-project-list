import xml.etree.ElementTree as ET
import urllib2 
import time
from datetime import date
import ConfigParser
import requests

# Get variables from the config file
config = ConfigParser.RawConfigParser()
config.read('project.conf')
projectsURL = config.get('General Information', 'projectsURL')
exportName = config.get('General Information', 'outputfile') 

"""
Class that will hold the various feeds

If you would like the xml form the url, call 
  .getxml()
The url can be found by calling
  .geturl()
"""
class tracksfeed(object):
    def __init__(self, url):
        self.url = url

    def geturl(self):
        return self.url
    def getxml(self):
        return requests.get(self.url).text

projects = tracksfeed(projectsURL)
root = ET.fromstring(projects.getxml())



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
