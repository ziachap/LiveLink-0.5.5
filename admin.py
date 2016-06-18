from django.contrib import admin
from models import *

# Register your models here.
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'venue', 'start_time')

class VenueAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'email', 'website')

class ArtistAdmin(admin.ModelAdmin):
    list_display = ('name', 'genre')

class DistributorBrandInline(admin.StackedInline):
    model = DistributorBrand
    can_delete = False
    verbose_name_plural = 'distributorbrand'

class DistributorAdmin(admin.ModelAdmin):
    list_display = ('link',)

class DistributorBrandAdmin(admin.ModelAdmin):
    list_display = ('name',)

# User/Profile inline

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'profile'

class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'first_name', 'last_name')
    inlines = (ProfileInline,)

# Register admin models
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Venue, VenueAdmin)
admin.site.register(Artist, ArtistAdmin)
admin.site.register(Distributor, DistributorAdmin)
admin.site.register(DistributorBrand, DistributorBrandAdmin)