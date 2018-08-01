from django.shortcuts import render, get_object_or_404, redirect, render_to_response
from .models import ParkingSpaceType, ParkingLot, ParkingSpace, StandaloneParkingSpace, UserOwnedParking, Vehicle, Ticket, Profile
from django.views import generic
from django.contrib.auth.decorators import login_required, permission_required
from .forms import ProfileForm, TicketForm, ParkingSpaceTicketForm
from django.views.generic.edit import CreateView, DeleteView, UpdateView, FormView
from django.urls import reverse_lazy 
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.http import HttpResponseRedirect, JsonResponse
from django.utils import timezone

#For google maps
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.core.serializers import serialize
from django.conf import settings
from .serializers import ExtJsonSerializer

# Create your views here.

#temporary index site to see a generic view of all the objects
def index(request):
    user_tickets = None
    if not request.user.is_anonymous:
            user_tickets = Ticket.objects.filter(person=request.user).order_by('-valid_to')
    num_parking_lot = ParkingLot.objects.all().count()
    num_parking_space = ParkingSpace.objects.all().count()
    num_vehicles = Vehicle.objects.all().count()
    num_tickets = Ticket.objects.all().count()

    return render(
        request,
        'index.html',
        context={'user_tickets':user_tickets,'num_parking_lot':num_parking_lot, 'num_parking_space':num_parking_space, 'num_vehicles':num_vehicles, 'num_tickets':num_tickets}
    )


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)     
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('profile-update', pk=user.profile.id)
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def parking(request):
    parking_lots = ParkingLot.objects.all()
    parking_lots.update()
    standalone_parking = StandaloneParkingSpace.objects.all()
    userowned_parking = UserOwnedParking.objects.all()

    parking_lot = ExtJsonSerializer().serialize(ParkingLot.objects.all(), fields=['name', 'latitude', 'longitude', 'price', 'opening_time', 'closing_time',
    'capacity_car', 'capacity_motorbike', 'car_taken'])
    parking_lot_json = json.dumps(list(parking_lot), cls = DjangoJSONEncoder)
    standalone = StandaloneParkingSpace.objects.all().values_list('latitude', 'longitude', 'price', 'opening_time', 'closing_time', 'status', 'id')
    standalone_json = json.dumps(list(standalone), cls=DjangoJSONEncoder)
    userowned = UserOwnedParking.objects.all().values_list('latitude', 'longitude', 'price', 'opening_time', 'closing_time', 'status', 'owner')
    userowned_json = json.dumps(list(userowned), cls=DjangoJSONEncoder)

    parking_lot_all_json = ExtJsonSerializer().serialize(ParkingLot.objects.all(), fields=['name', 'latitude', 'longitude', 'price', 'opening_time', 'closing_time',
    'capacity_car', 'capacity_motorbike', 'car_taken'])

    return render(
        request,
        'parking.html',
        context={'parking_lots':parking_lots, 
        'standalone_parking':standalone_parking, 
        'userowned_parking':userowned_parking, 
        'parking_lot_json':parking_lot_json, 
        'standalone_json':standalone_json,
        'userowned_json': userowned_json,
        'parking_lot_all_json': parking_lot_all_json}
    )

@login_required
def plticket(request, pk):
    parkinglot = get_object_or_404(ParkingLot, pk=pk)
    parkingspace = ParkingSpace.objects.filter(parking_lot = parkinglot, status='a').first()
    parkingspace.set_status('r')
    return psticket(request, parkingspace.id)
    
@login_required
def psticket(request, pk):
    parkingspace = get_object_or_404(ParkingSpace, pk=pk)    
    user = request.user
    ticket = Ticket()
    form = ParkingSpaceTicketForm(request.POST or None, instance=ticket)
    ticket.parking_space=parkingspace
    ticket.person = user
    ps_type = parkingspace.parking_type
    if(ps_type == 'c'):
        form.fields['vehicle'].queryset = Vehicle.objects.filter(owner=user, car=True)
    elif (ps_type == 'm'):
        form.fields['vehicle'].queryset = Vehicle.objects.filter(owner=user, motorbike=True)

    if form.is_valid():
        ticket.save()
        #Updating the related parkingspace
        parkingspace.set_taken_to(ticket.valid_to)
        parkingspace.set_status('t')
        parkingspace.set_taken_by(user)
        parkingspace.save()
        return render(request, 'parkingsystem/ticket_detail.html', {'ticket':ticket, 'parkingspace':parkingspace})   
    #GET
    return render(request, 'psticket.html', {'form':form})

@login_required
def ticket(request):
    user = request.user
    form = TicketForm(request.POST or None)

    #TODO: Add the filter on vehicletype
    form.fields['vehicle'].queryset = Vehicle.objects.filter(owner=user)
    if form.is_valid():
        data = form.cleaned_data
        ticket = Ticket(valid_to=data['valid_to'],parking_space=data['parkingspace'], vehicle=data['vehicle'], person=user)
        ticket.save()
        #Updating the related parkingspace
        parkingspace = data['parkingspace']
        parkingspace.set_taken_to(ticket.valid_to)
        parkingspace.set_status('t')
        parkingspace.set_taken_by(user)
        parkingspace.save()
        return render(request, 'parkingsystem/ticket_detail.html', {'ticket':ticket, 'parkingspace':parkingspace} )
        
    return render(request, 'parkingsystem/custom_ticketform.html', {'form':form})

#For dropdown
def load_parkingspace(request):
    parkinglot = request.GET.get('parkinglot')
    parkingspaces = ParkingSpace.objects.filter(parking_lot = parkinglot, status='a')
    return render(request, 'parkingsystem/parkingspace_dropdown.html', {'parkingspaces':parkingspaces})

#For dropdown
def load_vehicles(request):
    parkingspace_id = request.GET.get('parkingspace')
    parkingspace = get_object_or_404(ParkingSpace, pk=parkingspace_id)
    user = request.user
    ps_type = parkingspace.parking_type
    if(ps_type == 'c'):
        vehicles = Vehicle.objects.filter(owner=user, car=True)
    elif (ps_type == 'm'):
        vehicles = Vehicle.objects.filter(owner=user, motorbike=True)
    return render(request, 'parkingsystem/vehicle_dropdown.html', {'vehicles':vehicles})

def load_ps_price(request):
    parkingspace_id = request.GET.get('parkingspace')
    parkingspace = get_object_or_404(StandaloneParkingSpace, pk=parkingspace_id)
    data = {
        'price': parkingspace.price
    }
    return JsonResponse(data)

def load_pl_price(request):
    parkinglot_id = request.GET.get('parkinglot')
    parkinglot = get_object_or_404(ParkingLot, pk=parkinglot_id)
    data = {
        'price': parkinglot.price
    }
    return JsonResponse(data)

def terminate_ticket(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)
    ticket.valid_to = timezone.now()
    ticket.save()
    ticket.parking_space.taken_to = timezone.now()
    ticket.parking_space.save()
    return render(request, 'index.html')

class ParkingLotListView(generic.ListView):
    model = ParkingLot

class ParkingLotDetailView(generic.DetailView):
    model = ParkingLot

class ParkingSpaceListView(generic.ListView):
    model = ParkingSpace
class ParkingSpaceDetailView(generic.DetailView):
    model = ParkingSpace

"""
Parkingspace
"""
class StandaloneParkingSpaceCreate(CreateView):
    model = StandaloneParkingSpace
    fields = ['parking_type', 'latitude', 'longitude', 'price', 'opening_time', 'closing_time']

class StandaloneParkingSpaceUpdate(UpdateView):
    model = StandaloneParkingSpace

class StandaloneParkingSpaceDetailView(generic.DetailView):
    model = StandaloneParkingSpace

class StandaloneParkingSpaceDelete(DeleteView):
    model = StandaloneParkingSpace

class StandaloneParkingSpaceListView(generic.ListView):
    model = StandaloneParkingSpace

"""
Profile specific views
"""

class ProfileDetailView(LoginRequiredMixin, generic.ListView):
    model = Profile
    template_name = 'parkingsystem/profile.html'
    
class ProfileUpdate(UpdateView):
    model = Profile
    fields = ['mobile_number', 'birthdate', 'address', 'city', 'zip_code']
    
"""
Vehicles
"""

class VehicleDetailView(generic.DetailView):
    model = Vehicle

class VehicleListView(generic.ListView):
    model = Vehicle

class VehicleCreate(LoginRequiredMixin, CreateView):
    model = Vehicle
    fields = ['registration_number', 'brand', 'model', 'car', 'motorbike']

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(VehicleCreate, self).form_valid(form)

class VehicleUpdate(UpdateView):
    model = Vehicle
    fields = ['registration_number', 'brand', 'model', 'car', 'motorbike']

class VehicleDelete(DeleteView):
    model = Vehicle
    success_url = reverse_lazy('index')

"""
UserOwnedParkingSpaces
"""

class UserOwnedParkingDetailView(LoginRequiredMixin, generic.DetailView):
    model = UserOwnedParking

class UserOwnedParkingCreate(CreateView):
    model = UserOwnedParking
    fields = ['parking_type', 'latitude', 'longitude', 'price', 'opening_time', 'closing_time']

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(UserOwnedParkingCreate, self).form_valid(form)

class UserOwnedParkingUpdate(UpdateView):
    model = UserOwnedParking
    fields = ['parking_type', 'latitude', 'longitude', 'price', 'opening_time', 'closing_time']

class UserOwnedParkingDelete(DeleteView):
    model = UserOwnedParking
    success_url = reverse_lazy('index')

"""
Tickets
"""
class TicketDetailView(generic.DetailView):
    model = Ticket

class TicketListView(generic.ListView):
    model = Ticket

class TicketCreate(LoginRequiredMixin, CreateView):
    # Create a function that 
    model = Ticket
    fields = ['valid_to', 'parking_space', 'vehicle']
    
    def get_form(self, *args, **kwargs):
        form = super(TicketCreate, self).get_form(*args, **kwargs)
        form.fields['vehicle'].queryset = Vehicle.objects.filter(owner = self.request.user)
        form.fields['parking_space'].queryset = ParkingSpace.objects.filter(status = 'a')
        return form

    def get_user(self):
        return self.request.user

    def form_valid(self, form):
        form.instance.person = self.request.user
        ps = form.instance.parking_space
        ps.set_taken_to(form.instance.valid_to)
        ps.set_status('t')
        ps.set_taken_by(self.request.user)
        return super(TicketCreate, self).form_valid(form)

class TicketUpdate(UpdateView):
    model = Ticket
    fields = ['valid_to']

    def form_valid(self, form):
        form.instance.person = self.request.user
        ps = form.instance.parking_space
        ps.set_taken_to(form.instance.valid_to)
        ps.set_status('t')
        ps.set_taken_by(self.request.user)
        return super(TicketUpdate, self).form_valid(form)

"""
Classes for admin: 
Create parkinglot, parkingspace
Update parkinglot, parkingspace
see all tickets
See all cars
See all profiles/users
"""

class ParkingLotCreate(generic.CreateView):
    model = ParkingLot
    fields = '__all__'


    class Meta:
        if hasattr(settings, 'GOOGLE_MAPS_API_KEY') and settings.GOOGLE_MAPS_API_KEY:
            css = {
                'all': ('css/admin/location_picker.css',),
            }
            js = (
                'https://maps.googleapis.com/maps/api/js?key={}'.format(settings.GOOGLE_MAPS_API_KEY),
                'js/admin/location_picker.js',
            )