import requests, pprint, json
from bs4 import BeautifulSoup, NavigableString, Tag

# URL = "https://en.wikipedia.org/wiki/List_of_Hindu_temples_in_India"

# page = requests.get(URL)

# soup = BeautifulSoup(page.content, 'html.parser')

# results = soup.find(class_='mw-parser-output').find_all('ul')

# read file
fileRead = open('./templeLinks.txt', 'r')
lines = fileRead.readlines()

cnt = 0
for line in lines:
    cnt += 1
    if cnt > 100 :
        break
    URL = line.strip()
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, 'html.parser')
    
    # Temple Dictionary
    temple = {
        "address": "",
        "city": "",
        "createdBy": "Aryan",
        "country": "",
        "deity": "",
        "religion": "",
        "shortDescription": "",
        "detailedDescription": "",
        "headerImageUrl": "",
        "templeName": "",
        "websiteUrl": URL,
        "isActive": "0",
        "isApproved": "0",
        "region": "",
        "rank": "0",
        "businessHours": "0"
    }
    # image 
    img = soup.find(class_='infobox-image')
    if img :
        img = img.find('a')
        if img:
            img = img.find('img')
            if img.has_attr('src'):
                temple['headerImageUrl'] = "https:" + img['src']
    
    # templeName
    templeName = soup.find('h1')
    if templeName :
        temple["templeName"] = templeName

    results = soup.find(class_='infobox vcard')
    if results == None:
        continue
    results = results.find('tbody').find_all('tr')
    if results == None:
        continue
    i = 0

    for child in results:
        i += 1
        # templeName
        if i == 1 and child.find('th'):
            temple["templeName"] = child.find('th').string
        
        # religion
        if child.find('th') and child.find('th').find('a') and child.find('th').find('a').string == "Affiliation"  and child.find('td') and child.find('td').find('a'):
            temple["religion"] = child.find('td').find('a').string
        
        # religion
        if child.find('th') and child.find('th').find('a') and child.find('th').find('a').string == "Affiliation"  and child.find('td') and child.find('td').string:
            temple["religion"] = child.find('td').string
        
        # deity
        if child.find('th') and child.find('th').find('a') and child.find('th').find('a').string == "Deity" and child.find('td') and child.find('td').find('a'):
            temple["deity"] = child.find('td').find('a').string

        # deity
        if child.find('th') and child.find('th').find('a') and child.find('th').find('a').string == "Deity" and child.find('td') and child.find('td').string:
            temple["deity"] = child.find('td').string

        # country
        if child.find('th') and child.find('th').string == "Country" and child.find('td') and child.find('td').string :
            temple["country"] = child.find('td').string
        
        # country
        if child.find('th') and child.find('th').string == "Country" and child.find('td') and child.find('td').find('a') :
            temple["country"] = child.find('td').find('a').string
                
        # state
        if child.find('th') and child.find('th').string == "State" and child.find('td') and child.find('td').string:
            temple["region"] = child.find('td').string

        # state
        if child.find('th') and child.find('th').string == "State" and child.find('td') and child.find('td').find('a'):
            temple["region"] = child.find('td').find('a').string

        # city(location in td -> a)
        if child.find('th') and (child.find('th').string == "Location") and child.find('td') and child.find('td').find('a'):
            temple["city"] = child.find('td').find('a').string
        
        # city(location in td)
        if child.find('th') and (child.find('th').string == "Location") and child.find('td') and child.find('td').string:
            temple["city"] = child.find('td').string

        # city(district)
        if child.find('th') and (child.find('th').string == "District") and child.find('td') and child.find('td').find('a'):
            temple["city"] = child.find('td').find('a').string
        
        # city(district)
        if child.find('th') and (child.find('th').string == "District") and child.find('td') and child.find('td').string:
            temple["city"] = child.find('td').string
    
    # Description
    des = soup.find(class_ = 'mw-parser-output')
    des = des.find_all(['p', 'h2'])
    for pInDes in des:
        if isinstance(pInDes, NavigableString) :
            continue
        if pInDes.name == 'h2' :
            break
        elif isinstance(pInDes, Tag) :
            # print(pInDes.get_text())
            if pInDes.get_text() == None or pInDes.get_text() == '\n' :
                continue
            f = 1
            for c in pInDes.get_text():
                if c != None and c == '[' :
                    f = 1-f
                if f and c != None:
                    temple["detailedDescription"] += c
                if c != None and c == ']' :
                    f = 1-f
            # pInDes.find_all(['b', 'a'])
            # for aInDes in pInDes:
            #     if aInDes.string is not None and aInDes.string[0] != ' ':
            #         print("#" + aInDes.string + "#")
            #         temple["detailedDescription"] += aInDes.string
    # print(temple["detailedDescription"])
    temple["shortDescription"] = temple["detailedDescription"][0:min(200, len(temple["detailedDescription"]))]
    if temple["city"] != "" and temple["city"] is not None and temple["region"] != "" and temple["region"] is not None and temple["country"] != "" and temple["country"] is not None and temple["templeName"] != "" and temple["templeName"] is not None and temple["deity"] != "" and temple["deity"] is not None and temple["religion"] != "" and temple["religion"] is not None and temple["shortDescription"] != "" and temple["shortDescription"] is not None and temple["detailedDescription"] != "" and temple["detailedDescription"] is not None:
        print(json.dumps(temple, indent=4, sort_keys=True) + ",")