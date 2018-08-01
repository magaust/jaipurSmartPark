from django.conf import settings
from django.contrib import admin
from django.utils import timezone

# Register your models here.
from .models import Profile, ParkingSpaceType, ParkingLot, ParkingSpace, StandaloneParkingSpace, UserOwnedParking, Vehicle, Ticket

class ParkingSpaceAdmin(admin.ModelAdmin):
    list_display=['id', 'parking_lot', 'parking_type', 'status', 'is_available', 'taken_to']

    class Media:
        if hasattr(settings, 'GOOGLE_MAPS_API_KEY') and settings.GOOGLE_MAPS_API_KEY:
            css = {
                'all': ('css/admin/location_picker.css',),
            }
            js = (
                'https://maps.googleapis.com/maps/api/js?key={}'.format(settings.GOOGLE_MAPS_API_KEY),
                'js/admin/location_picker.js',
            )

class ParkingLotAdmin(admin.ModelAdmin):
    list_display=['name', 'latitude', 'longitude','car_taken']

    class Media:
        if hasattr(settings, 'GOOGLE_MAPS_API_KEY') and settings.GOOGLE_MAPS_API_KEY:
            css = {
                'all': ('css/admin/location_picker.css',),
            }
            js = (
                'https://maps.googleapis.com/maps/api/js?key={}'.format(settings.GOOGLE_MAPS_API_KEY),
                'js/admin/location_picker.js',
            )

class StandaloneParkingSpaceAdmin(admin.ModelAdmin):
    list_display=['id', 'latitude', 'longitude']

    class Media:
        if hasattr(settings, 'GOOGLE_MAPS_API_KEY') and settings.GOOGLE_MAPS_API_KEY:
            css = {
                'all': ('css/admin/location_picker.css',),
            }
            js = (
                'https://maps.googleapis.com/maps/api/js?key={}'.format(settings.GOOGLE_MAPS_API_KEY),
                'js/admin/location_picker.js',
            )

class UserOwnedParkingAdmin(admin.ModelAdmin):
      class Media:
        if hasattr(settings, 'GOOGLE_MAPS_API_KEY') and settings.GOOGLE_MAPS_API_KEY:
            css = {
                'all': ('css/admin/location_picker.css',),
            }
            js = (
                'https://maps.googleapis.com/maps/api/js?key={}'.format(settings.GOOGLE_MAPS_API_KEY),
                'js/admin/location_picker.js',
            )

class TicketAdmin(admin.ModelAdmin):
    list_display=['person', 'parking_space', 'valid_to']
    #TODO: Delete method - change taken_to in related parking_space.

    def delete_selected(self, request, obj):
        for o in obj.all():
            o.parking_space.taken_to = timezone.now()
            o.parking_space.save()
            o.delete()

    actions = ['delete_selected']


admin.site.register(Profile)
admin.site.register(ParkingSpaceType)
admin.site.register(ParkingLot, ParkingLotAdmin)
admin.site.register(ParkingSpace, ParkingSpaceAdmin)
admin.site.register(StandaloneParkingSpace, StandaloneParkingSpaceAdmin)
admin.site.register(UserOwnedParking, UserOwnedParkingAdmin)
admin.site.register(Vehicle)
admin.site.register(Ticket, TicketAdmin) 