from bs4 import BeautifulSoup
import requests
import json
import re


allInfo = {"Austin": {}, "New York": {}, "Washington": {}} #dictionary to store camp info for each location

austinURL = "https://austinsummercamps.org/" #url for austin summer camps
austinResult = requests.get(austinURL)
austinDoc = BeautifulSoup(austinResult.text, "html.parser")

austinInfo = {} #dictionary to hold the camp provider and website links for austin


camps = austinDoc.find_all("a", href=True) #find all links with href
for link in camps:
    onclick = link.get('onclick', '')
    href = link.get('href', '')  #the url that we want
    target = link.get_text(strip=True)  #camp name
    
    if onclick:
        eventLabelMatch = re.search(r"'event_label':\s*'([^']+)'", onclick)
        if eventLabelMatch:
            eventLabel = eventLabelMatch.group(1)
            #filter out entries that are just website domains and entries that look like domains
            if ("@" not in eventLabel and target and href.startswith('http') and len(target) > 3 and target not in austinInfo and not target.startswith('www.') and not target.endswith('.com') and not target.endswith('.org') and not target.endswith('.edu') and not target.endswith('.net') and
                not re.match(r'^[a-zA-Z0-9.-]+\.(com|org|edu|net)$', target) and
                #keep entries that look like actual camp names (have spaces or descriptive words)
                (len(target.split()) > 1 or 
                 any(word in target.lower() for word in ['camp', 'summer', 'academy', 'school', 'center', 'studio']))):
                
                austinInfo[target] = href #add names and links to the dictionary with austin info

#remove duplicates by checking if URLs are the same
#keep the more descriptive name for each unique URL
urlToName = {}
for name, url in austinInfo.items():
    if url in urlToName:
        existingName = urlToName[url]
        if len(name) > len(existingName):
            urlToName[url] = name
    else:
        urlToName[url] = name

#rebuild austinInfo with deduplicated entries
austinInfo = {name: url for url, name in urlToName.items()}

#store Austin info
allInfo["Austin"] = austinInfo



dcURL = "https://dcsummercamps.com/" #link for dc info
dcResult = requests.get(dcURL)
dcDoc = BeautifulSoup(dcResult.text, "html.parser")

dcInfo = {}

#find all links with href (same pattern as Austin)
camps = dcDoc.find_all("a", href=True)
for link in camps:
    onclick = link.get('onclick', '')
    href = link.get('href', '')  
    target = link.get_text(strip=True)  
    
    if onclick:
        eventLabelMatch = re.search(r"'event_label':\s*'([^']+)'", onclick)
        if eventLabelMatch:
            eventLabel = eventLabelMatch.group(1)
            
            #filter out website domains and keep only actual camp names
            if ("@" not in eventLabel and target and href.startswith('http') and len(target) > 3 and target not in dcInfo and
                not target.startswith('www.') and not target.endswith('.com') and not target.endswith('.org') and not target.endswith('.edu') and not target.endswith('.net') and not re.match(r'^[a-zA-Z0-9.-]+\.(com|org|edu|net)$', target) and
                #keep entries that look like actual camp names (have spaces or descriptive words)
                (len(target.split()) > 1 or 
                 any(word in target.lower() for word in ['camp', 'summer', 'academy', 'school', 'center', 'studio']))):
                
                dcInfo[target] = href #add names and websites to dictionary for dc

#remove duplicates by checking if URLs are the same and keep the more descriptive name for each unique URL
urlToName = {}
for name, url in dcInfo.items():
    if url in urlToName:
        existingName = urlToName[url]
        if len(name) > len(existingName):
            urlToName[url] = name
    else:
        urlToName[url] = name

dcInfo = {name: url for url, name in urlToName.items()}

allInfo["Washington"] = dcInfo #store DC info in big dictionary


nycURL = "https://manhattansummercamps.com/" #nyc url (manhattan)
nycResult = requests.get(nycURL)
nycDoc = BeautifulSoup(nycResult.text, "html.parser")

nycInfo = {}

#find all links with href 
camps = nycDoc.find_all("a", href=True)
for link in camps:
    onclick = link.get('onclick', '')
    href = link.get('href', '') 
    target = link.get_text(strip=True) 
    
    if onclick:
        eventLabelMatch = re.search(r"'event_label':\s*'([^']+)'", onclick)
        if eventLabelMatch:
            eventLabel = eventLabelMatch.group(1)
            
            if ("@" not in eventLabel and target and href.startswith('http') and len(target) > 3 and target not in nycInfo and
                not target.startswith('www.') and not target.endswith('.com') and not target.endswith('.org') and not target.endswith('.edu') and
                not target.endswith('.net') and not re.match(r'^[a-zA-Z0-9.-]+\.(com|org|edu|net)$', target) and
                (len(target.split()) > 1 or 
                 any(word in target.lower() for word in ['camp', 'summer', 'academy', 'school', 'center', 'studio']))):
                
                nycInfo[target] = href

urlToName = {}
for name, url in nycInfo.items():
    if url in urlToName:
        existingName = urlToName[url]
        if len(name) > len(existingName):
            urlToName[url] = name
    else:
        urlToName[url] = name

nycInfo = {name: url for url, name in urlToName.items()}

allInfo["New York"] = nycInfo

with open('camps.json', 'w') as file: #save to json file
    json.dump(allInfo, file, indent=2)
