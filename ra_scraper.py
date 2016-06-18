import requests, os, sys
import bs4, urllib, re
from django.core.files import File
from models import *
import dateutil.parser

# RESIDENT ADVISOR SCRAPER

def scrapeAllEvents(url):
    response = requests.get(url)
    soup = bs4.BeautifulSoup(response.text, "html.parser")
    links = [a.attrs.get('href') for a in soup.select('a[href^=/event.aspx?]')]

    author = User.objects.get(username='ziachap')
    #print links

    for i, l in enumerate(links):
        print "Scraping ", i, "/", len(links),"events"
        link_url = 'https://www.residentadvisor.net' + l
        print link_url
        title, type, date, venue, desc, cover, venue_link = scrapeEventPage(link_url)

        # Skip if event already exists, else make a new one
        event = Event.objects.filter(name=title)
        print event
        if not event:
            print "making new event"
            # find the venue, if not there, scrape its info and add it
            venue_object = Venue.objects.filter(name=venue)
            if not venue_object:
                vurl = 'https://www.residentadvisor.net' + venue_link
                print venue_link
                print vurl
                vtitle, vdesc, vlon, vlat, logo, vwebsite, vaddress, vemail = scrapeVenuePage(vurl)
                venue_object = Venue(name=vtitle,email=vemail,summary=vdesc,location=vaddress,longitude=vlon,latitude=vlat,website=vwebsite)
                # Grab the logo image
                if logo:
                    result = urllib.urlretrieve(logo)
                    venue_object.logo.save(
                        os.path.basename(logo),
                        File(open(result[0]))
                    )
                venue_object.save()
                print "Added Venue:",vtitle
            else:
                venue_object = venue_object[0]


            # Make the new EVENT object
            event = Event(name=title, start_time=date, author=author,venue=venue_object,type=type,description=desc)
            # Grab the cover image
            if cover != []:
                result = urllib.urlretrieve(cover)
                event.cover.save(
                        os.path.basename(cover),
                        File(open(result[0]))
                        )
            event.save()
            print "saved new event"

def scrapeEventPage(url):
    response = requests.get(url)
    soup = bs4.BeautifulSoup(response.text, "html.parser")
    #print "HTML: ",soup

    # TITLE
    title = soup.select('div#sectionHead h1')[0].get_text().encode('utf8')

    # DESCRIPTION
    desc = soup.select('div.left p')[1]
    [s.extract() for s in desc('div')]
    for e in desc.findAll('br'):
        e.extract()
    desc = desc.get_text().encode('utf8')

    # DATE/TIME
    time = soup.select('aside#detail ul.clearfix li')[0]
    [s.extract() for s in time('div')]
    time = time.get_text().encode('utf8')[-13:-8]

    date = soup.select('ul.clearfix li a')[0]
    [s.extract() for s in date('div')]
    date = date.get_text().encode('utf8')
    datetime = dateutil.parser.parse(date+' '+time)

    # VENUE
    venue = soup.select('li.wide a')
    venue_link = venue
    if venue != []:
        venue = venue[0].get_text().encode('utf8')
        venue_link = soup.select('a[href^=/club.aspx?]')[0].attrs.get('href').encode('utf8')
        print venue_link

    # TYPE
    type = 'Club Night'

    # EXTERNAL COVER IMAGE
    #cover = ""
    cover = soup.select('div.flyer a img')
    if cover != []:
        cover = 'https://www.residentadvisor.net' + cover[0].attrs.get('src').encode('utf8')

    return title, type, datetime, venue, desc, cover, venue_link

def getVenueLinks(url):
    response = requests.get(url)
    soup = bs4.BeautifulSoup(response.text, "html.parser")
    return [a.attrs.get('href') for a in soup.select('a[href^=/club.aspx?]')]

def scrapeAllVenues(url):
    response = requests.get(url)
    soup = bs4.BeautifulSoup(response.text, "html.parser")
    links = [a.attrs.get('href') for a in soup.select('a[href^=/club.aspx?]')]

    for i, l in enumerate(links):
        print "Scraping ", i, "/", len(links)
        link_url = 'https://www.residentadvisor.net' + l
        title, desc, lon, lat, cover, website, address, email = scrapeVenuePage(link_url)

        # Try and find the venue, else make a new one
        venue = Venue.objects.get(name=title)
        if venue == []:
            venue = Venue(name=title,email=email,summary=desc,location=address,longitude=lon,latitude=lat,website=website)
            # Grab the logo image
            if cover != []:
                result = urllib.urlretrieve(cover)
                venue.logo.save(
                    os.path.basename(cover),
                    File(open(result[0]))
                )
                venue.save()
        

def scrapeVenuePage(url):
    response = requests.get(url)
    soup = bs4.BeautifulSoup(response.text, "html.parser")

    # TITLE
    title = soup.select('div#sectionHead h1')[0].get_text().encode('utf8')

    # DESCRIPTION
    desc = soup.select('div.fl div[style^=padding]')[0].get_text().encode('utf8')

    # LOCATION
    lat = soup.select('div#divMap input')[0].attrs.get('value').encode('utf8')
    lon = soup.select('div#divMap input')[1].attrs.get('value').encode('utf8')

    # ADDRESS
    address = soup.select('span[itemprop=street-address]')[0].get_text().encode('utf8')

    # WEBSITE
    website = soup.findAll('a', text = re.compile('Website'))
    if website != []:
        website = website[0].attrs.get('href').encode('utf8')

    # EMAIL
    email = soup.findAll('a', text = re.compile('Email'))
    if email != []:
        email = email[0].attrs.get('href').encode('utf8')
        email = email.split(':')[1]

    # EXTERNAL COVER IMAGE
    cover = ""
    #cover = 'https://www.residentadvisor.net' + soup.select('div.flyer a img')[0].attrs.get('src')
    cover = soup.select('div.plus8 div.clearfix div.fl img')
    print "COVER: ",cover
    if cover != []:
        cover = 'https://www.residentadvisor.net' + cover[0].attrs.get('src')

    return title, desc, lon, lat, cover, website, address, email

#scrapeAllVenues('https://www.residentadvisor.net/clubs.aspx')
#scrapeAllEvents('https://www.residentadvisor.net/events.aspx')





