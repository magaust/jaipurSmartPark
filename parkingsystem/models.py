from django.db import models
import uuid # required for unique parkingspace
from django.contrib.auth.models import User, Permission

#for post save when creating a parking lot:
from django.db.models.signals import post_save
from django.dispatch import receiver

#to generate urls
from django.urls import reverse
from django.utils import timezone

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile_number = models.CharField(max_length=20, blank=True, null=True)
    address = models.CharField(max_length=150, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    zip_code = models.PositiveIntegerField(blank=True, null=True)
    birthdate = models.DateField(blank=True, null=True)
    
    #TODO: DEL
    total_income = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return self.user.__str__()

    def get_absolute_url(self):
        return reverse('home', args=[str(self.id)])

    def profit(self, amount):
        self.total_income += amount

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)
    
    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

#TODO: Kan slettes
class ParkingSpaceType(models.Model):
    """
    Model representing a type of parkingspace(e.g. Car, motorbike, etc)
    """
    parking_type = models.CharField(max_length=150, unique=True)
    def __str__(self):
        """
        String for representing the Model object (in Admin site etc.)
        """
        return self.parking_type

class ParkingLot(models.Model):
    """
    Model representing a parking lot which can have mant parkingspaces
    """
    #ID field added automatically
    #TODO: add mb_space_taken and add it into maps.
    name = models.CharField(max_length=150, null=True, blank=True)
    price = models.PositiveIntegerField()
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    opening_time = models.TimeField()
    closing_time = models.TimeField()
    rfid = models.PositiveIntegerField()
    capacity_car = models.PositiveIntegerField()
    capacity_motorbike = models.PositiveIntegerField()
    car_space_taken = models.PositiveIntegerField()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('parkinglot-detail', args=[str(self.id)])

    @property
    def car_taken(self):
        return ParkingSpace.objects.filter(parking_lot=self, parking_type='c', status='t').count()
    
    @property
    def mb_taken(self):
        return ParkingSpace.objects.filter(parking_lot=self, parking_type='m', status='t').count()

class ParkingSpaceManager(models.Manager):
    def get_avail_parking(self):
        return self.filter(status='a')

class ParkingSpace(models.Model):
    TYPES = (
        ('c', 'Car'),
        ('m', 'Motorbike'),
    ) 
    parking_type = models.CharField(max_length=1, choices=TYPES, null=True)
    parking_lot = models.ForeignKey(ParkingLot, on_delete=models.CASCADE, null=True, blank=True)
    taken_to = models.DateTimeField(auto_now_add=True)

    STATUS = (
        ('t', 'Taken'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )
    #TODO: Delete status/ change the use to property is_available.
    status = models.CharField(max_length=1, choices=STATUS, blank=True, default='a', help_text='Parking space availability')

    def __str__(self):
        """
        String for representing the Model object (in Admin site etc.)
        """
        return str(self.id)

    def get_absolute_url(self):
        """
        Returns the url to access a detail record for this parking space.
        """
        return reverse('parkingspace-detail', args=[str(self.id)])

    def set_status(self,status):
        if (status == 't' or status == 'a' or status == 'r'):
            self.status = status
            self.save()
        return

    def set_taken_by(self, person):
        self.taken_by = person
        self.save()

    def set_taken_to(self, dateTime):
        self.taken_to = dateTime
        self.save()

    @property
    def is_available(self):
        if self.taken_to and timezone.now() > self.taken_to:
            self.set_status('a')
            return True
        return False

class StandaloneParkingSpace(ParkingSpace):
    """
    Subclass of parkingspace representing a parking space outside a parkingLot
    """
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    price = models.PositiveIntegerField()
    opening_time = models.TimeField()
    closing_time = models.TimeField()

    def __str__(self):
        return str(self.id)

    def get_absolute_url(self):
        """
        Returns the url to access a detail record for this parking space.
        """
        return reverse('standalone-detail', args=[str(self.id)])

class UserOwnedParking(StandaloneParkingSpace):
    """
    A standalone parking space which can be owned by an user to rent out.
    """
    owner = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.owner.__str__() +" parking")
       
    def get_absolute_url(self):
        """
        Returns the url to access a detail record for this parking space.
        """
        return reverse('userparking-detail', args=[str(self.id)])

class Vehicle(models.Model):
    registration_number = models.CharField(max_length=50, unique=True)
    brand = models.CharField(max_length=150)
    model = models.CharField(max_length=150)
    car = models.BooleanField()
    motorbike = models.BooleanField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.registration_number

    def get_absolute_url(self):
        return reverse('vehicle-detail', args=[str(self.id)])

class Ticket(models.Model):
    start = models.DateTimeField(auto_now_add=True)
    valid_to = models.DateTimeField()
    # On_delete Gjøres noe med før deployment??
    parking_space = models.ForeignKey(ParkingSpace, on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    person = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.vehicle.owner.__str__()

    def get_absolute_url(self):
        return reverse('ticket-detail', args=[str(self.id)])

    @property
    def is_valid(self):
        if self.valid_to and timezone.now() < self.valid_to:
            self.parking_space.set_status("a")
            return True
        return False

    @property
    def duration_in_minutes(self):
        duration = self.valid_to - self.start
        return int(duration.seconds/60)

    #TODO: slettes?
    @property
    def price(self):
        try:
            price = self.parking_space.parking_lot.price * self.duration_in_minutes
        except AttributeError:
            return 0
        return int(price)

"""
Function to create parkingspaces when creating a parking lot. Uses a post_save signal on parking lot.
"""
def create_parking_space_for_parking_lot(sender, instance, **kwargs):
    if kwargs['created']:
        for x in range(0,instance.capacity_car):
            parking_space = ParkingSpace.objects.create(parking_type = 'c', parking_lot=instance)
        for y in range(0, instance.capacity_motorbike):
            parking_space = ParkingSpace.objects.create(parking_type = 'm', parking_lot=instance)

post_save.connect(create_parking_space_for_parking_lot, sender=ParkingLot)
