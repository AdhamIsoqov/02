# Generated by Django 5.1.6 on 2025-03-20 09:29

import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Guest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('age', models.IntegerField(default=20)),
                ('phone', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Hotel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('phone', models.CharField(max_length=10)),
                ('city', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_no', models.IntegerField(default=101)),
                ('room_type', models.CharField(default='standard', max_length=200)),
                ('rate', models.FloatField()),
                ('is_available', models.BooleanField(default=True)),
                ('no_of_beds', models.IntegerField(default=3)),
                ('hotel', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='hotels.hotel')),
            ],
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('checkin_date', models.DateTimeField(default=datetime.datetime(2025, 3, 20, 14, 29, 30, 624846))),
                ('checkout_date', models.DateTimeField(default=datetime.datetime(2025, 3, 21, 14, 29, 30, 624846))),
                ('check_out', models.BooleanField(default=False)),
                ('no_of_guests', models.IntegerField(default=1)),
                ('guest', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hotels.guest')),
                ('hotel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hotels.hotel')),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hotels.room')),
            ],
        ),
    ]
