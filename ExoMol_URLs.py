#import packages required for script to run
import requests,urllib.request, os, string
from bs4 import BeautifulSoup
from datetime import datetime

#set URLMOL as the starting URL where all the ExoMol Molecules are found
URLMOL = "http://exomol.com/data/molecules/"


#this section obtains all URL extensions available on the molecules page, and then extracts just the 
#molecule extensions through the if statement
r = requests.get(URLMOL)
soup = BeautifulSoup(r.content, "lxml")  #list of url extensions

ftype = ['trans','states','pf','models','def']
mol = []

for link in soup.find_all('a'):
   
    r = link.get('href')
    
    if len(r) < 6 and len(r) > 1:  #checking for extension length
        mol.append(r)
    else:
        pass
        
print('Molecules found!')

#this section creates an array imp[] which has obtained all the istopologues for each molecule
#and has added this extension to the molecule URL
nex = []
new = []
imp = []

for x in mol:
    
    URLM = URLMOL + x 
    new.append(URLM)
    
    r = requests.get(URLM)
    soup = BeautifulSoup(r.content, "lxml")

    
    for link in soup.find_all('a'): #gets url extensions
        r = link.get('href')
    
        if len(r) <= 12 and r.find('/') ==-1: #extracts isotopologue url extensions
            nex.append(r)
            URLN = URLMOL + x + '/' + r
            imp.append(URLN)
        else:
            pass
print('Isotopologues found!')

#this section goes into each istopologue and extracts the line list URL, this is where the files are stored
wow = []
links = []
for x in imp:
    
    r = requests.get(x)
    soup = BeautifulSoup(r.content, "lxml")


    for link in soup.find_all('a'):
        r = link.get('href')
    
        if len(r) <= 12 and r.find('/') ==-1:
            URLX = x + '/' + r
            wow.append(URLX)
        else:
            pass
        
print('Line Lists found!')

#this section obtains all the URLs for the states, trans, pf and def files for each isotpologue
#for each molecule. However it also obtains the URLs for the Model files, which leads to a new section
#where these are stored

links = []
for x in wow:
    
    r = requests.get(x)
    soup = BeautifulSoup(r.content, "lxml")


    for link in soup.find_all('a'):
        r = link.get('href')
        
        for c in ftype:
            if c in r:
                URLZ = 'http://exomol.com/' + str(r)
                links.append(URLZ)
            else:
                pass
        
print('Links found, almost there!')

#this finds all the model URL's, goes into this link, obtains the file URL's and replaces the Model
#URL's with the file URL's in the array
mod = []
for x in links:
        if 'model' in x:
            mod.append(x)
            
print('Model links extracted')

inp = []
key = 'inp'

for x in mod:
    
    r = requests.get(x)
    soup = BeautifulSoup(r.content, "lxml")

    for link in soup.find_all('a'):
        r = link.get('href')
        if key in r:
            URLMO = 'http://exomol.com' + r
            inp.append(URLMO)
        
print('Model files found')

for model in mod:
    links.remove(model)

all_URLs = links + inp

#all_URLs contains all the file URL's available on the ExoMol database
print('all file URL\'s have been obtained!')

#the following extracts just the files for a specific molecule
#delete the double hashtags and replace 'MOLECULE' with what molecule you want data for

##MOLECULE = []        
##for x in all_URLs:
    ##if 'MOLECULE' in x:
        ##MOLECULE.append(x)

#the following extracts specific files e.g. trans/states/pf/inp
#delete the double hashtags and replace 'FILE' with what file type you want data for

##FILE = []
##for x in all_URLs:
    ##if 'FILE' in x:
        ##FILE.append(x)
        
#Sets a variable to an empty array
nofile = []


    
#downloads the files into current working directory
#all_URLs can and probably should be replaced with a speficic molecule/file URL list
#otherwise you will be downloading ALOT of files which takes up ALOT of space!!!
#delete the double hashtags but ensure you are downloading what you want to download not every file (unless you want every file)

##for x in all_URLs:
    ##file_name = x.split('/')[-1]
    ##try:
        ##urllib.request.urlretrieve(x, file_name)
    ##except:
        ##print('Failed to download', file_name)