from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from stdimage.models import StdImageField


class Venue(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=256, null=False, blank=False)
    summary = models.TextField(max_length=2000, null=True, blank=True)
    location = models.TextField(max_length=1000, null=True, blank=True)
    longitude = models.DecimalField(decimal_places=16, max_digits=28, default=-0.1275)
    latitude = models.DecimalField(decimal_places=16, max_digits=28, default=51.5072)
    website = models.URLField(max_length=500, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    logo = StdImageField(upload_to='venue_logos/', null=True, blank=True, variations={
        'thumbnail': (300, 300, True),
    })
    #default="/static/images/default_venue.jpg", 
    cover = StdImageField(upload_to='venue_covers/', null=True, blank=True, variations={
        'large' : {"width": 1200, "height": 320, "crop": True, "resize": True},
        'thumbnail': (300, 300, True),
    })
    def __str__(self):
        return "%s" % self.name

class Artist(models.Model):
    name = models.CharField(max_length=128, null=False, blank=False)
    bio = models.TextField(max_length=1000, null=True, blank=True)
    GENRES = (
      ('Pop', 'Pop'),
      ('Reggae', 'Reggae'),
      ('Folk', 'Folk'),
      ('R&B/Soul', 'R&B/Soul'),
      ('Jazz', 'Jazz'),
      ('Indie', 'Indie'),
      ('Metal', 'Metal'),
      ('Rock', 'Rock'),
      ('Garage', 'Garage'),
      ('Drum & Bass', 'Drum & Bass'),
      ('House', 'House'),
      ('Hip Hop/Rap', 'Hip Hop/Rap'),
      ('Dubstep', 'Dubstep'),
      ('Grime', 'Grime'),
      ('Electronic', 'Electronic'),
      ('Dance', 'Dance'),
      ('Classical', 'Classical'),
      ('Gospel', 'Gospel'),
    )
    genre = models.CharField(max_length=64, choices=GENRES, null=True)
    fb_link = models.URLField(max_length=500, null=True, blank=True)
    sc_link = models.URLField(max_length=500, null=True, blank=True)
    yt_link = models.URLField(max_length=500, null=True, blank=True)
    embed_sc = models.URLField(max_length=500, null=True, blank=True)
    logo = StdImageField(upload_to='venue_logos/', null=True, blank=True, variations={
        'thumbnail': (300, 300, True),
    })
    cover = StdImageField(upload_to='artist_logos/', null=True, blank=True, variations={
        'large' : (1200,320),
        'thumbnail': (300, 300, True),
    })
    def __str__(self):
        return "%s" % self.name


class Event(models.Model):
    id = models.AutoField(primary_key=True)
    author = models.ForeignKey(User, null=True, related_name='author')
    name = models.CharField(max_length=128, null=False, blank=False)
    artists = models.ManyToManyField(Artist, null=True, blank=True, related_name='artists')
    venue = models.ForeignKey(Venue, null=True)
    TYPES = (
        ('Club Night', 'Club Night'),
        ('Live Music', 'Live Music'),
        ('Festival', 'Festival'),
    )
    type = models.CharField(max_length=64, choices=TYPES, null=True)
    description = models.TextField(max_length=2000, null=True, blank=True)
    start_time = models.DateTimeField(blank=False, default=timezone.now)
    end_time = models.DateTimeField(blank=True, null=True)
    fb_link = models.URLField(max_length=500, null=True, blank=True)
    cover = StdImageField(upload_to='event_logos/', variations={
        'icon' : (32,32, True),
        'banner' : (600,160, True),
        'large' : (1200,320),
        'thumbnail': (300, 300, True),
    })
    def __str__(self):
        return "%s" % self.name

# Extends default user profile to provide additional data
class Profile(models.Model):
    user = models.OneToOneField(User)
    bio = models.TextField(max_length=1000, null=True, blank=True)
    profile_pic = StdImageField(upload_to='profile_pictures/', null=True, blank=True, variations={
        'thumbnail': (300, 300, True),
    })
    artist_following = models.ManyToManyField(Artist, null=True, blank=True, related_name='artist_following')
    venue_following = models.ManyToManyField(Venue, null=True, blank=True, related_name='venue_following')
    def __str__(self):
        return "%s" % self.user.username

class DistributorBrand(models.Model):
    name = models.CharField(max_length=128, null=False, blank=False)
    logo = StdImageField(upload_to='distributor_logos/', null=True, blank=True, variations={
        'thumbnail': (300, 300, True),
    })
    def __str__(self):
        return "%s" % self.name

class Distributor(models.Model):
    event = models.ForeignKey(Event, null=True)
    distributor = models.ForeignKey(DistributorBrand, null=True, blank=False)
    price = models.IntegerField(null=True, blank=False)
    link = models.URLField(max_length=500, null=True, blank=True)
    def __str__(self):
        return "%s" % self.distributor.name

