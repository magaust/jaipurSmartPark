from django import forms
from django.contrib.auth.models import User
from .models import Profile, Vehicle, Ticket, ParkingSpace, ParkingLot
from django.contrib.admin.widgets import AdminDateWidget

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('birthdate', 'mobile_number', 'address', 'city', 'zip_code')

class ParkingSpaceForm(forms.ModelForm):
    class Meta:
        model = ParkingSpace
        fields = ('parking_lot',)

class TicketForm(forms.Form):
    parkinglot  = forms.ModelChoiceField(queryset=ParkingLot.objects.all())
    parkingspace = forms.ModelChoiceField(queryset=ParkingSpace.objects.all())
    vehicle = forms.ModelChoiceField(queryset=Vehicle.objects.all())
    valid_to = forms.DateTimeField(widget = AdminDateWidget) # change widget

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        #If no parkinglot -> show only standalone parkingspaces.
        self.fields['parkingspace'].queryset = ParkingSpace.objects.filter(parking_lot=None, status='a')

        if 'parkinglot' in self.data:
            try:
                parkinglot_id = int(self.data.get('parkinglot'))
                self.fields['parkingspace'].queryset = ParkingSpace.objects.filter(parking_lot=parkinglot_id)
            except (ValueError, TypeError):
                pass

class ParkingSpaceTicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['vehicle', 'valid_to']
