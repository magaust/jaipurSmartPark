from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('overview/', views.parking, name='parking'),
    path('profile/<int:pk>/update/', views.ProfileUpdate.as_view(), name ='profile-update'),
    path('profile/<int:pk>', views.ProfileDetailView.as_view(), name='home'),
    path('signup/', views.signup, name='signup'),
]
#  path('home', views.home, name='home'),

#Parkinglots
urlpatterns += [
    path('parkinglots/', views.ParkingLotListView.as_view(), name='parkinglots'),
    path('parkinglot/<int:pk>', views.ParkingLotDetailView.as_view(), name='parkinglot-detail'),
    path('parkinglot/add/', views.ParkingLotCreate.as_view(), name='parkinglot-add'),
    path('parkinglot/<int:pk>/ticket/', views.plticket, name='plticket'),
]

#Parkingspaces
urlpatterns += [
    path('parkinglot/parkingspace/<int:pk>', views.ParkingSpaceDetailView.as_view(), name='parkingspace-detail'),
    path('standaloneparking/add/', views.StandaloneParkingSpaceCreate.as_view(), name='standalone-add'),
    path('standaloneparking/<int:pk>/update/', views.StandaloneParkingSpaceUpdate.as_view(), name='standalone-update'),
    path('standaloneparking/<int:pk>/delete/', views.StandaloneParkingSpaceDelete.as_view(), name='standalone-delete'),
    path('standaloneparking/<int:pk>', views.StandaloneParkingSpaceDetailView.as_view(), name='standalone-detail'),
    path('standaloneparking/<int:pk>/ticket/', views.psticket, name='psticket'),
]

#Vehicles
urlpatterns += [
    path('vehicles/', views.VehicleListView.as_view(), name='vehicles'),
    path('vehicle/<int:pk>/', views.VehicleDetailView.as_view(), name='vehicle-detail'),
    path('vehicle/add/', views.VehicleCreate.as_view(), name='vehicle-add'),
    path('vehicle/<int:pk>/update/', views.VehicleUpdate.as_view(), name='vehicle-update'),
    path('vehicle/<int:pk>/delete', views.VehicleDelete.as_view(), name='vehicle-delete')
]

#UserOwnedParkingSpace
urlpatterns += [
    path('myparkingspace/<int:pk>/', views.UserOwnedParkingDetailView.as_view(), name='userparking-detail'),
    path('myparkingspace/add/', views.UserOwnedParkingCreate.as_view(), name='userparking-add'),
    path('myparkingspace/<int:pk>/update/', views.UserOwnedParkingUpdate.as_view(), name='userparking-update'),
    path('myparkingspace/<int:pk>/delete/', views.UserOwnedParkingDelete.as_view(), name='userparking-delete'),
]

#Tickets (for users. Can only see their own tickets)
urlpatterns += [
    path('tickets/', views.TicketListView.as_view(), name='tickets'),
    path('ticket/<int:pk>/', views.TicketDetailView.as_view(), name='ticket-detail'),
    path('ticket/add/', views.ticket, name='ticket-add'),
    path('ticket/<int:pk>/update/', views.TicketUpdate.as_view(), name='ticket-update'),
    path('ticket/<int:pk>/terminate', views.terminate_ticket, name='ticket-terminate'),
    path('ajax/load-parkingspaces/', views.load_parkingspace, name='ajax-load-parkingspace'),
    path('ajax/load-vehicles/', views.load_vehicles, name='ajax-load-vehicle'),
    path('ajax/load-pl-price/', views.load_pl_price, name='ajax-load-pl-price'),
    path('ajax/load-ps-price/', views.load_ps_price, name='ajax-load-ps-price'),
]

#Need a listview for staff which can see all the tickets.
