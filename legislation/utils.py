# CA Legislature web scraper
# Magnus Haw April 6, 2021
import requests
from bs4 import BeautifulSoup
from dateutil import parser
from django_cron import CronJobBase, Schedule
from .models import Legislator, Session, Hearing, Bill, Committee
from datetime import timedelta
from django.utils import timezone

def saveAgenda(sorted_agendas, house):
    billstxt = "A.B. 1035,A.B. 1069,A.B. 1087,A.B. 11,A.B. 1110,A.B. 1124,A.B. 1139,A.B. 1147,A.B. 1161,A.B. 117,A.B. 1177,A.B. 1201,A.B. 1218,A.B. 1238,A.B. 125,A.B. 1260,A.B. 1270,A.B. 1276,A.B. 1289,A.B. 1312 ,A.B. 1317,A.B. 1325,A.B. 1346,A.B. 1365,A.B. 1384,A.B. 1389,A.B. 1395,A.B. 1397,A.B. 1401,A.B. 1453,A.B. 1500,A.B. 1559,A.B. 20,A.B. 220,A.B. 222,A.B. 284,A.B. 322,A.B. 33,A.B. 352,A.B. 353,A.B. 37,A.B. 39,A.B. 427,A.B. 43,A.B. 467,A.B. 478,A.B. 5,A.B. 50,A.B. 51,A.B. 52,A.B. 525,A.B. 53,A.B. 55,A.B. 558,A.B. 564,A.B. 585,A.B. 64,A.B. 648,A.B. 67,A.B. 680,A.B. 683,A.B. 699,A.B. 713,A.B. 72,A.B. 745,A.B. 766,A.B. 776,A.B. 802,A.B. 818,A.B. 842,A.B. 843,A.B. 881,A.B. 896,A.B. 897,A.B. 906,A.B. 96,A.B. 962,A.B. 965,A.B. 992,AJR-4,S.B. 1,S.B. 18,S.B. 204,S.B. 25,S.B. 260,S.B. 261,S.B. 27,S.B. 29,S.B. 30,S.B. 31,S.B. 32,S.B. 339,S.B. 342,S.B. 343,S.B. 345,S.B. 359,S.B. 372,S.B. 38,S.B. 406,S.B. 413,S.B. 416,S.B. 419,S.B. 423,S.B. 429,S.B. 437,S.B. 439,S.B. 439,S.B. 44,S.B. 449,S.B. 45,S.B. 467,S.B. 47,S.B. 474,S.B. 475,S.B. 479,S.B. 500,S.B. 506,S.B. 527,S.B. 529,S.B. 533,S.B. 54,S.B. 542,S.B. 551,S.B. 560,S.B. 580,S.B. 582,S.B. 589,S.B. 595,S.B. 596,S.B. 599,S.B. 612,S.B. 617,S.B. 643,S.B. 66,S.B. 662,S.B. 67,S.B. 671,S.B. 68,S.B. 726,S.B. 730,S.B. 733,S.B. 771,S.B. 83,S.B. 84,S.B. 99,A.B. 1177"
    follows = billstxt.split(',')
    session, session_created = Session.objects.get_or_create(house=house,year_start=timezone.now().year,year_end=timezone.now().year+1)
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
            if bill['title'] in follows:
                mybill, bill_created = Bill.objects.get_or_create(name=bill['title'],session = session)
                if bill_created:
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

            
