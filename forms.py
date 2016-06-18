from models import *
from django.contrib.auth.models import User
from django import forms

# Define forms here
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ('username', 'password', 'first_name', 'last_name', 'email')

class EditUserProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('bio', 'profile_pic')

class VenueForm(forms.ModelForm):
    class Meta:
        model = Venue
        fields = ('name', 'summary', 'location', 'longitude', 'latitude', 'website', 'email', 'logo', 'cover')

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ('name', 'description', 'venue', 'type', 'start_time', 'end_time', 'fb_link', 'cover')

class EditEventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ('name', 'description', 'venue', 'type', 'start_time', 'end_time', 'fb_link', 'cover')

class RAForm(forms.Form): #Note that it is not inheriting from forms.ModelForm
    url = forms.URLField(max_length=256)
    #All my attributes here