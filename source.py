import bs4 as bsoup
import urllib.request as request
import re
import datetime
import csv

link = "https://en.wikipedia.org/wiki/2019_in_spaceflight#Orbital_launches"
data = request.urlopen(link).read()
soup = bsoup.BeautifulSoup(data, 'lxml')
orbitals_table = soup.find('table', {'class':'wikitable collapsible'})
rows = orbitals_table.find_all('tr')

##Defining constants
months = {'january':1,'february':2,'march':3,'april':4,
         'may':5,'june':6,'july':7,'august':8,
         'september':9,'october':10,'november':11,'december':12}

data_regex = '([0-9][0-9]* [a-zA-Z]*)'
pattern_date = re.compile(data_regex)
pattern_operation = re.compile('([a-zA-Z]*)')
allowed_orbitals = {'operational','successful','en route'}

def getIso(date):
    ans = datetime.datetime(date.year, date.month, date.day)
    return ans.isoformat()

def getDate(key):
    key = pattern_date.split(key)
    date = key[1].split(' ')
    day, month = date[0], months.get(date[1].lower())
    return datetime.date(2019, month, int(day))

def writeToCsv(summary):
    with open('orbitals.csv', mode='w') as orbitals_file:
        sdate = datetime.date(2019, 1, 1)   # start date
        edate = datetime.date(2019, 12, 31)   # end date
        diff = edate - sdate
        for i in range(diff.days+1):
            day = sdate + datetime.timedelta(days=i)
            if(day in summary):
                orbitals_file.write("%s, %s\n"%(str(getIso(day)), summary[day]))
            else:
                orbitals_file.write("%s, %s\n"%(str(getIso(day)), 0))


parsed = []
for row in rows[3:]:
    td = row.find_all('td')
    check_table = row.findAll("table",{"class":"navbox hlist"})
    if(check_table):
        continue
    td_text = [column.text.strip() for column in td]
    parsed.append(td_text)

## Remove unneccessary remarks from the dataset
filtered_date = list(filter(lambda x:len(x) > 1, parsed))
length = len(filtered_date)
counter = 0
summarized = {}

while counter < length:
    date = filtered_date[counter][0]
    num_orbitals = []
    counter += 1

    while counter < length and len(filtered_date[counter]) == 6:
        parsed_data = filtered_date[counter]
        if parsed_data[5] != None:
            status = pattern_operation.search(parsed_data[5]).group()
            if status.lower() in allowed_orbitals:
                num_orbitals.append(parsed_data)
        counter += 1
    
    date_ = getDate(date)
    if(len(num_orbitals) > 0):
        if date_ in summarized:
            summarized[date_] += 1 
        else:
            summarized[date_] = 1

writeToCsv(summarized)