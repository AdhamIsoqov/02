from django.db import models
from datetime import datetime, timedelta
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.validators import MinValueValidator, MaxValueValidator


# Mehmon modeli
class Guest(models.Model):
    name = models.CharField(max_length=200)
    age = models.IntegerField(default=20)
    phone = models.CharField(max_length=10)

    def __str__(self):
        return self.name


# Mehmonxona modeli
class Hotel(models.Model):
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=10)
    city = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
      # Hozirgi mehmonxonani tekshiruvdan chiqaramiz (exclude)
        if Hotel.objects.filter(name=self.name).exclude(id=self.id).exists():
            raise ValueError(f"{self.name} mehmonxonasi allaqachon mavjud!")
        super().save(*args, **kwargs)



# Xona modeli
class Room(models.Model):
    ROOMS_TYPES = [
        ("ST", "STANDART"),
        ("CF", "COMFORT"),
        ("LX", "LUXE"),
    ]

    room_no = models.IntegerField(default=101)
    hotel = models.ForeignKey(Hotel, null=True, on_delete=models.CASCADE)
    room_type = models.CharField(choices=ROOMS_TYPES, max_length=10)
    rate = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)],
        help_text="Xona reytingini 0 dan 5 gacha, masalan, 4.7 shaklida kiriting."
    )
    is_available = models.BooleanField(default=True)
    no_of_beds = models.IntegerField(default=3)

    def __str__(self):
        return f"{self.hotel.name} - Xona {self.room_no}"

    def hotel_name(self):
        return self.hotel.name

    def save(self, *args, **kwargs):
      # Xuddi shu mehmonxona va xona raqamiga ega boshqa obyekt mavjudligini tekshiramiz
        if Room.objects.filter(room_no=self.room_no, hotel=self.hotel).exclude(id=self.id).exists():
            raise ValueError(f"Xona {self.room_no} {self.hotel.name} mehmonxonasida allaqachon mavjud!")
            super().save(*args, **kwargs)



# Band qilish modeli
class Booking(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    guest = models.ForeignKey(Guest, on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    checkin_date = models.DateTimeField(default=datetime.now)
    checkout_date = models.DateTimeField(default=lambda: datetime.now() + timedelta(days=1))
    check_out = models.BooleanField(default=False)
    no_of_guests = models.IntegerField(default=1)

    def __str__(self):
        return f"Booking by {self.guest.name} for {self.room}"

    def charge(self):
        if self.check_out:
            if self.checkin_date == self.checkout_date:
                return self.room.rate
            else:
                time_delta = self.checkout_date - self.checkin_date
                total_time = time_delta.days
                total_cost = total_time * self.room.rate
                return total_cost
        else:
            return "calculated when checked out"


# Xona band bo'lganidan keyin holatini yangilash
@receiver(post_save, sender=Booking)
def update_room_availability(sender, instance, created, **kwargs):
    room = instance.room
    if created:
        room.is_available = False
    if instance.check_out:
        room.is_available = True
    room.save()
