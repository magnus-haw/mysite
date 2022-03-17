# CA Legislature web scraper
# Magnus Haw April 6, 2021
import requests
from bs4 import BeautifulSoup
from dateutil import parser
from django_cron import CronJobBase, Schedule
from .models import Legislator, Session, Hearing, Bill, Committee, Sector
from datetime import timedelta
from django.utils import timezone
import pandas as pd
from re import findall

def getCurrentSession(house):
    session, session_created = Session.objects.get_or_create(house=house,year_start=timezone.now().year,year_end=timezone.now().year+1)
    return session

def saveAgenda(sorted_agendas, house):
    session = getCurrentSession(house)
    for hr in sorted_agendas:
        committee, com_created = Committee.objects.get_or_create(name = hr['name'])
        if com_created:
            committee.link = hr['link']
            committee.save()

        myhearing, hearing_created = Hearing.objects.get_or_create(date=hr['date'], session = session, committee=committee)
        if hearing_created:
            myhearing.letter_due_date = hr['date'] - timedelta(days=7)
            myhearing.link=hr['link']
        myhearing.time=hr['time']
        myhearing.location=hr['location']
        myhearing.save()
        
        for bill in hr['bills']:
            if bill['title'] in session.follows:
                mybill, bill_created = Bill.objects.get_or_create(name=bill['title'],session = session)
                if 1:
                    mybill.number = int(bill['title'].split(' ')[-1])
                    mybill.author=bill['author']
                    mybill.description=bill['description']
                    mybill.link=bill['link']
                    mybill.save()
                myhearing.bills.add(mybill)

def getSenateCommitteeLinks(URL = "https://www.senate.ca.gov/committees"):
    cpage = requests.get(URL)
    csoup = BeautifulSoup(cpage.content,'lxml')
    clinks = csoup.find('div',id='block-views-committees-standing').find('div','view-content').find_all('a')
    committees = [{'link':link['href'], 'Name':link.string} for link in clinks]
    return committees

def parseSenateRosterRow(row):
    ntitle = row.find('div', 'views-field-field-senator-last-name').find('h3').string
    nsplit = ntitle.split('(')
    name = nsplit[0].strip()
    if nsplit[1] =='D)':
        party = 'Democrat'
    elif nsplit[1] =='R)':
        party = 'Republican'
    else:
        party = 'Independent'

    district_div = row.find('div', 'views-field-field-senator-district').find('div', 'field-content')
    rm_span = district_div.find('span'); rm_span.extract()
    district = int(district_div.string.strip())

    webpage = row.find('div', 'views-field-field-senator-weburl').find('a')['href']
    contact = row.find('div', 'views-field-field-senator-feedbackurl').find('a')['href']

    capitol_office = row.find('div', 'views-field-field-senator-capitol-office').find_all('p')[-1]
    rm_br = capitol_office.find_all('br'); [br.extract() for br in rm_br]
    district_office = row.find('div', 'views-field-field-senator-district-office').find_all('p')[-1]
    rm_br = district_office.find_all('br'); [br.extract() for br in rm_br]

    senator_dict = {'name':name,'party':party, 'district':district, 'webpage':webpage, 'contact':contact,
            'capitol_office':capitol_office.text, 'district_office':district_office.text}
    print(senator_dict)
    senator, _created = Legislator.objects.get_or_create(name=name, party=party, district=district, webpage=webpage, contact=contact,
                                                         capitol_office=capitol_office.text, district_office=district_office.text)
    
    return senator_dict

def getSenateRoster(URL = "https://www.senate.ca.gov/senators"):
    cpage = requests.get(URL)
    csoup = BeautifulSoup(cpage.content,'lxml')
    rows = csoup.find('div',id="block-views-senator-roster-block").find('div','view-content').find_all('div',"views-row")

    senators = [parseSenateRosterRow(row) for row in rows]

    return senators

def parseSenateMeasureRow(row):
    link = row.find('a')['href']
    author = row.find('span', 'Author').string
    mtype = row.find('a').find("span",'MeasureType').string
    mnumber = row.find('a').find("span", 'MeasureNum').contents[1]
    title = mtype + mnumber
    description = row.find('span', 'Topic').string

    return {"title":title, "link":link, "author":author, "description":description}

def parseSenateMeeting(meet,URL,cname):
    date_str = meet.find("div","calendarDate").string
    date = parser.parse(date_str)
    agenda = meet.find("div","SDF230")
    time = agenda.find("div", "agenda_hearingTime").string
    location = agenda.find("div", "agenda_hearingLocation").string
    rows = agenda.find_all("span", "Measure row")

    bills = [parseSenateMeasureRow(row) for row in rows]

    return {'name':cname, 'link':URL, "date":date,"time":time, "location":location, "bills":bills}

def getSenateCommitteeAgenda(soup, URL):
    cname = soup.find('div','banner-sitename').find('a').string
    meets = soup.find_all("div", "calendarDayContainer list-group")

    allhearings = [parseSenateMeeting(meet,URL,cname) for meet in meets]

    return allhearings

def getFullSenateAgenda():
    committees = getSenateCommitteeLinks()
    agendas = []
    for committee in committees:
        URL = committee['link']
        if URL[-1] != '/':
            URL += '/agenda'
        else:
            URL += 'agenda'
        page = requests.get(URL)
        soup = BeautifulSoup(page.content,'lxml')
        scom_agenda = getSenateCommitteeAgenda(soup, URL)
        agendas += scom_agenda
    sorted_agendas = sorted(agendas, key = lambda item:item.get('date'))
    saveAgenda(sorted_agendas, "Senate")
    return sorted_agendas

def getAssemblyCommitteeLinks(URL = "https://www.assembly.ca.gov/committees"):
    cpage = requests.get(URL)
    csoup = BeautifulSoup(cpage.content,'lxml')
    clinks = csoup.find('div',id='block-views-view_StandingCommittee-block_1').find('div','view-content').find_all('a')
    committees = [{'link':link['href'], 'Name':link.string} for link in clinks]
    return committees

def parseAssemblyMeasureRow(row):
    link = row.find('a')['href']
    author = row.find('span', 'Author').string
    mtype = row.find('a').find("span",'MeasureType').string
    mnumber = row.find('a').find("span", 'MeasureNum').contents[1]
    title = mtype + mnumber
    description = row.find('span', 'Topic').string

    return {"title":title, "link":link, "author":author, "description":description}

def parseAssemblyMeeting(agenda,date,URL,cname):
    date = parser.parse(date.string)
    time = agenda.find("div", "agenda_hearingTime").string
    location = agenda.find("div", "agenda_hearingLocation").string
    rows = agenda.find_all("span", "Measure")

    bills = [parseAssemblyMeasureRow(row) for row in rows]

    return {"name":cname, "link":URL, "date":date,"time":time, "location":location, "bills":bills}

def getAssemblyCommitteeAgenda(soup,URL):
    cname = soup.find('a','com').string

    try:

        block = soup.find('h2',text="Committee Hearings ").parent
        dates = block.find_all('h5')
        meets = block.find_all("div", "ADF130")

        allhearings = [parseAssemblyMeeting(meet,date,URL,cname) for meet,date in zip(meets,dates)]
    except:
        allhearings = []
    return allhearings

def getFullAssemblyAgenda():
    committees = getAssemblyCommitteeLinks()
    agendas = []
    for committee in committees:
        URL = committee['link']
        if URL[-1] != '/':
            URL += '/hearings'
        else:
            URL += 'hearings'
        page = requests.get(URL)
        soup = BeautifulSoup(page.content,'lxml')
        ascom_agenda = getAssemblyCommitteeAgenda(soup,URL)
        agendas += ascom_agenda
        sorted_agendas = sorted(agendas, key = lambda item:item.get('date'))
    saveAgenda(sorted_agendas,"Assembly")
    return sorted_agendas


class MyCronJob(CronJobBase):
    RUN_EVERY_MINS = 480 # every 8 hours

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'legislation.my_cron_job'    # a unique code

    def do(self):
        getFullAssemblyAgenda()
        getFullSenateAgenda()

def uploadBills(dataframe):
    for index, row in dataframe.iterrows():
        #clean name
        name = row['Bill']
        named = clean_bill_name(name)
        cname = named['clean']
    
        author = row['Author']
        description = row['Title']
        sectorname = row['Sector'].lower()
        # get or create sector
        sector,sector_created = Sector.objects.get_or_create(name=sectorname)
        session = getCurrentSession(named['house'])
        bill,bcreated = Bill.objects.get_or_create(name=cname, session=session)
        bill.description = description
        bill.sector = sector
        bill.author = author
        bill.save()

def clean_bill_name(name):
    name = name.upper()
    house,number = findall(r'([A-Z\.]+)(?:[_ -]*)(\d+)', name)[0]
    ret = {'#':int(number), 'name':name}
    if 'S' in house:
        ret['house'] = 'Senate'
        if 'B' in house:
            ret['clean'] = "S.B. %s"%(number)
        else:
            ret['clean'] = "%s %s"%(house,number)
    elif 'A' in house and 'B' in house:
        ret['house'] = 'Assembly'
        ret['clean'] = "A.B. %s"%(number)
    else:
        ret['house'] = 'Unknown'
        ret['clean'] = name
    
    return ret