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
username = config.get('General Information', 'username') 
password = config.get('General Information', 'password') 

class tracksfeed(object):
    def __init__(self, url):
        self.url = url

    def geturl(self):
        return self.url
    def getxml(self):
        return requests.get(self.url, auth=(username, password)).text

projects = tracksfeed(projectsURL)
root = ET.fromstring(projects.getxml())

def createProjectList(xml):
    priority = 1 # set the variable
    for project in xml.findall('project'):
        projectState = project.find('state').text
        if projectState == 'active':
            projectName = project.find('name').text.title()
            with open(exportName, "a") as myfile:
                number = "%i. " % (int(priority))
                myfile.write(number)
                myfile.write(projectName)
                myfile.write('\n')
            priority = priority + 1
    print 'File should be saved, take a look at\n\n%s\n' % exportName

def createHeader():
    name = config.get('General Information', 'yourname')
    now = date.today()
    header = '# %s\'s projects as of %s\n\n' % (name,now)
    with open(exportName, 'w') as myfile:
        myfile.write(header)

createHeader()
createProjectList(root)
