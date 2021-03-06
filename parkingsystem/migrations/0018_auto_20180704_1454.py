# Generated by Django 2.0.6 on 2018-07-04 09:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('parkingsystem', '0017_auto_20180704_1339'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='parkinglot',
            name='car_space_taken',
        ),
        migrations.RemoveField(
            model_name='parkinglot',
            name='motorbike_space_taken',
        ),
        migrations.RemoveField(
            model_name='ticket',
            name='duration',
        ),
        migrations.AlterField(
            model_name='parkingspace',
            name='parking_lot',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='parkingsystem.ParkingLot'),
        ),
    ]
