# Generated by Django 2.0.6 on 2018-07-13 06:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('parkingsystem', '0021_ticket_amount'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ticket',
            name='amount',
        ),
    ]