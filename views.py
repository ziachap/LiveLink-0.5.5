from django.shortcuts import render
from django.template import loader, Context, RequestContext
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from django.core.files import File
import urllib
from forms import *
from models import *
from ra_scraper import *

# Create your views here.
#

def map(request):
    # Example - get the current user
    c_user = request.user
    users = User.objects.all()

    # Get all events ordered by date
    events = Event.objects.all().order_by('-start_time')

    # setup context
    context = RequestContext(request, {
                'c_user': c_user,
                'users': users,
                'events': events,
            })

    # Manage login request if POST request, otherwise go to index
    if request.method == 'POST':
        return user_login_inpage(request)
    else:
        t = loader.get_template('map.html')
        return HttpResponse(t.render(context))

def index(request):
    # Example - get the current user
    c_user = request.user
    users = User.objects.all()

    # Get all events ordered by date
    events = Event.objects.all().order_by('-start_time')

    # setup context
    context = RequestContext(request, {
                'c_user': c_user,
                'users': users,
                'events': events,
            })

    # Manage login request if POST request, otherwise go to index
    if request.method == 'POST':
        return user_login_inpage(request)
    else:
        t = loader.get_template('index.html')
        return HttpResponse(t.render(context))

def new(request):
    # setup context
    context = RequestContext(request, {
            })

    # Manage login request if POST request, otherwise go to index
    if request.method == 'POST':
        return user_login_inpage(request)
    else:
        t = loader.get_template('new.html')
        return HttpResponse(t.render(context))

def register(request):

    context = RequestContext(request)
    #If a post request, then we need to process some data
    if request.method == 'POST':

        form = UserForm(request.POST)

        if form.is_valid():

            user = form.save()
            user.set_password(user.password)
            user.save()
            prof = Profile(user = user)
            prof.save()

            user_login = authenticate(username=user.username, password=form.cleaned_data['password']
)
            print user_login
            if user_login:
                print("register: logging new user in");
                login(request, user_login)

            request.method = 'GET'
            return map(request)
        else:
            print form.errors
    else:
        form = UserForm()
    return render(request, 'register.html', {'form':form})

def venue(request, id):

    venue = Venue.objects.get(id=id);

    # Get all events ordered by date
    events = Event.objects.filter(venue=venue).order_by('-start_time').reverse();

    # setup context
    context = RequestContext(request, {
                'events': events,
                'venue' : venue
            })

    # get template
    t = loader.get_template('venue.html')
    return HttpResponse(t.render(context))

def event(request, id):

    # Get event
    event = Event.objects.get(id=id)

    # Get artists for event
    artists = event.artists.all();
    #event_qs = Event.objects.filter(artists__name='artists_name')
    #artists = Artist.objects.filter(event_set__in=event_qs)

    # Get ticket distributors
    distributors = Distributor.objects.filter(event=event)

    # setup context
    context = RequestContext(request, {
                'event': event,
                'distributors': distributors,
                'artists': artists
            })

    # get template
    t = loader.get_template('event.html')
    return HttpResponse(t.render(context))

def artist(request, name):

    artist = Artist.objects.get(name=name)

    # Get all events
    events = Event.objects.filter(artists__in=[artist])

    # setup context
    context = RequestContext(request, {
                'events': events,
                'artist': artist
            })

    # get template
    t = loader.get_template('artist.html')
    return HttpResponse(t.render(context))

def profile(request, name):

    # Get posts from everything the user follows
    # events = Event.objects.filter(artists__in=[artist])
    r_user = User.objects.get(username = name)

    # setup context
    context = RequestContext(request, {
            'r_user': r_user
            })

    # get template
    t = loader.get_template('profile.html')
    return HttpResponse(t.render(context))

def profile_edit(request):
    # get current user
    r_user = request.user
    r_profile = request.user.profile
    # get form
    form = EditUserProfileForm(instance=r_profile)

    # obtain the context for the user's request.
    context = RequestContext(request, {
                'r_user': r_user,
                'form': form
            })

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        print("views: POST")

        # create a form instance and populate it with data from the request:
        form = EditUserProfileForm(request.POST, request.FILES, instance=r_profile)

        # check whether it's valid:
        if form.is_valid():
            print("views: form valid")
            # copy extra info and save profile

            form.save();

            # switch request type and refresh
            request.method = 'GET'
            return profile(request, r_user.username)
        else:
            print form.errors

    # if a GET (or any other method) create a blank form
    t = loader.get_template('profile_edit.html')
    return HttpResponse(t.render(context))

def event_edit(request, id):
    # get current user
    r_event = Event.objects.get(id=id)
    # get form
    form = EditEventForm(instance=r_event)

    # obtain the context for the user's request.
    context = RequestContext(request, {
                'event': r_event,
                'form': form
            })

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        print("views: POST")

        # create a form instance and populate it with data from the request:
        form = EditEventForm(request.POST, request.FILES, instance=r_event)

        # check whether it's valid:
        if form.is_valid():
            print("views: form valid")
            # copy extra info and save profile

            form.save();

            # switch request type and refresh
            request.method = 'GET'
            return event(request, id)
        else:
            print form.errors

    # if a GET (or any other method) create a blank form
    t = loader.get_template('event_edit.html')
    return HttpResponse(t.render(context))

# For following artists and venues
def artist_follow(request, name):
    item = Artist.objects.get(name=name)
    request.user.profile.artist_following.add(item)
    return artist(request, name)
def artist_unfollow(request, name):
    item = Artist.objects.get(name=name)
    request.user.profile.artist_following.remove(item)
    return artist(request, name)

def venue_follow(request, id):
    item = Venue.objects.get(id=id)
    request.user.profile.venue_following.add(item)
    return venue(request, id)
def venue_unfollow(request, id):
    item = Venue.objects.get(id=id)
    request.user.profile.venue_following.remove(item)
    return venue(request, id)

def venue_new(request):
    # get form
    form = VenueForm()

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        print("views: POST")

        # create a form instance and populate it with data from the request:
        form = VenueForm(request.POST, request.FILES)

        # check whether it's valid:
        if form.is_valid():
            print("views: form valid")
            # set owner and save listing
            l = form.save(commit=False)
            #l.owner = c_user
            l.save();

            # switch request type and redirect to browse map
            return HttpResponseRedirect(reverse('map'))
        else:
            # get form
            form = VenueForm(request.POST)
            print form.errors

    # get the request's context.
    context = RequestContext(request, {
            'form': form,
    })

    # if a GET (or any other method) we'll create a blank form
    t = loader.get_template('venue_new.html')
    return HttpResponse(t.render(context))

def do_something(request):
    #scrapeAllVenues('https://www.residentadvisor.net/clubs.aspx')
    scrapeAllEvents('https://www.residentadvisor.net/events.aspx?ai=24')
    return new(request)

def venue_new_ra(request):
    # get url
    form = RAForm()
    success = False

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        print("views: POST")

        # create a form instance and populate it with data from the request:
        form = RAForm(request.POST, request.FILES)

        # check whether it's valid:
        if form.is_valid():
            print("views: form valid")
            # set owner and save listing
            #url = form.url
            url = form.cleaned_data['url']
            print url
            print "scraping..."

            # Scrape
            title, desc, lon, lat, cover, website, address, email = scrapeVenuePage(url)
            print title, desc, cover, website

            # Make the new venue object and save it
            venue = Venue(name=title,email=email,summary=desc,location=address,longitude=lon,latitude=lat,website=website)
            # Grab the logo image
            if cover != []:
                result = urllib.urlretrieve(cover)
                venue.logo.save(
                        os.path.basename(cover),
                        File(open(result[0]))
                        )            

            venue.save()

            success = True

        else:
            # get form
            form = RAForm(request.POST)
            print form.errors

    # get the request's context.
    context = RequestContext(request, {
        'form': form,
        'success': success,
    })

    # if a GET (or any other method) we'll create a blank form
    t = loader.get_template('new.html')
    return HttpResponse(t.render(context))

def event_new_ra(request):
    
    # get url
    form = RAForm()
    success = False

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        print("views: POST")

        # create a form instance and populate it with data from the request:
        form = RAForm(request.POST, request.FILES)

        # check whether it's valid:
        if form.is_valid():
            print("views: form valid")
            # set owner and save listing
            #url = form.url
            url = form.cleaned_data['url']
            print url
            print "scraping event..."

            # Scrape
            title, type, date, venue, desc, cover = scrapeEventPage(url)
            print title, desc

            # find the venue, if not there, add it
            venue_object = Venue.objects.get(name=venue)
            if venue_object == []:
                venue_object = Venue(name=venue, longitude=0, latitude=50)

            # Make the new venue object
            event = Event(name=title, start_time=date, author=request.user,venue=venue_object,type=type,description=desc)
            # Grab the cover image
            if cover != []:
                result = urllib.urlretrieve(cover)
                event.cover.save(
                        os.path.basename(cover),
                        File(open(result[0]))
                        )
            event.save()

            success = True

        else:
            # get form
            form = RAForm(request.POST)
            print form.errors

    # get the request's context.
    context = RequestContext(request, {
        'form': form,
        'success': success,
    })

    # if a GET (or any other method) we'll create a blank form
    t = loader.get_template('new.html')
    return HttpResponse(t.render(context))

def event_new(request):
    # get form
    form = EventForm()

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        print("views: POST")

        # create a form instance and populate it with data from the request:
        form = EventForm(request.POST, request.FILES)

        # check whether it's valid:
        if form.is_valid():
            print("views: form valid")
            # set owner and save listing
            l = form.save(commit=False)
            l.author = request.user
            l.save();

            # switch request type and redirect to browse map
            return HttpResponseRedirect(reverse('map'))
        else:
            # get form
            form = EventForm(request.POST)
            print form.errors

    # get the request's context.
    context = RequestContext(request, {
            'form': form,
    })

    # if a GET (or any other method) we'll create a blank form
    t = loader.get_template('event_new.html')
    return HttpResponse(t.render(context))

def user_login_inpage(request):
    print("POST Request - User Login")
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')

    user = authenticate(username=username, password=password)

    # If we have a User object, the details are correct.
    # If None (Python's way of representing the absence of a value), no user
    # with matching credentials was found.
    if user:
        # Is the account active? It could have been disabled.
        if user.is_active:
            # If the account is valid and active, we can log the user in.
            # We'll send the user back to the homepage.
            login(request, user)
            return HttpResponseRedirect(reverse('map'))
        else:
            # An inactive account was used - no logging in!
            return HttpResponse("Your account is disabled.")
    else:
        # Bad login details were provided. So we can't log the user in.
        print "Invalid login details: {0}, {1}".format(username, password)
        return HttpResponse("Invalid login details supplied.")

def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('map'))