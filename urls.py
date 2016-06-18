from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from livelink import views

urlpatterns = patterns('',

    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT,
    }),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.STATIC_ROOT,
    }),

    url(r'^admin/', include(admin.site.urls)),

    # Pages
    url(r'^map/', views.map, name='map'),
    url(r'^$', views.index, name='index'),

    # Generics
    url(r'^venue/(?P<id>[0-9]+)/$', views.venue, name='venue'),
    url(r'^event/(?P<id>[0-9]+)/$', views.event, name='event'),
    url(r'^artist/([\w ]+)/$', views.artist, name='artist'),
    url(r'^user/([\w ]+)/$', views.profile, name='profile'),

    # Forms
    url(r'^new/$', views.new, name='new'),
    url(r'^edituser/$', views.profile_edit, name='profile_edit'),
    url(r'^editevent/(?P<id>[0-9]+)/$', views.event_edit, name='event_edit'),
    url(r'^newvenue/$', views.venue_new, name='venue_new'),
    url(r'^newvenuera/$', views.venue_new_ra, name='venue_new_ra'),
    url(r'^dosomething/$', views.do_something, name='do_something'),
    url(r'^newevent/$', views.event_new, name='event_new'),
    url(r'^neweventra/$', views.event_new_ra, name='event_new_ra'),

    # Following
    url(r'^follow/([\w ]+)/$', views.artist_follow, name='artist_follow'),
    url(r'^unfollow/([\w ]+)/$', views.artist_unfollow, name='artist_unfollow'),
    url(r'^venuefollow/(?P<id>[0-9]+)/$', views.venue_follow, name='venue_follow'),
    url(r'^venueunfollow/(?P<id>[0-9]+)/$', views.venue_unfollow, name='venue_unfollow'),

    # Authentication
    url(r'^register/', views.register, name='register'),
    url(r'^logout/', views.user_logout, name='logout'),
)
