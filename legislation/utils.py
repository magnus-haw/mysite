# CA Legislature web scraper
# Magnus Haw April 6, 2021
import requests
from bs4 import BeautifulSoup
from dateutil import parser
from django_cron import CronJobBase, Schedule
from .models import Session, Hearing, Bill


def saveAgenda(sorted_agendas, house):
    ag = Session(house=house)
    ag.save()
    for hr in sorted_agendas:
        myhearing = Hearing(name=hr['name'], date=hr['date'], time=hr['time'], location=hr['location'], link=hr['link'], agenda=ag)
        myhearing.save()
        for bill in hr['bills']:
            mybill = Bill(title=bill['title'], author=bill['author'], description=bill['description'], link=bill['link'], hearing=myhearing)
            mybill.save()

def getSenateCommitteeLinks(URL = "https://www.senate.ca.gov/committees"):
    cpage = requests.get(URL)
    csoup = BeautifulSoup(cpage.content,'lxml')
    clinks = csoup.find('div',id='block-views-committees-standing').find('div','view-content').find_all('a')
    committees = [{'link':link['href'], 'Name':link.string} for link in clinks]
    return committees

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
    saveAgenda(sorted_agendas, 1)
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
    saveAgenda(sorted_agendas,2)
    return sorted_agendas



class MyCronJob(CronJobBase):
    RUN_EVERY_MINS = 5 # every 8 hours

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'legislation.my_cron_job'    # a unique code

    def do(self):
        getFullAssemblyAgenda()
        getFullSenateAgenda()

            