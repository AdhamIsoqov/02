from django.contrib import admin
from django.contrib import messages
from .models import Guest
from .models import Hotel
from .models import Room
from .models import Booking

@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'city']

    def save_model(self, request, obj, form, change):
        if not change and Hotel.objects.filter(name=obj.name).exists():
            messages.error(request, f"Mehmonxona '{obj.name}' allaqachon mavjud!")
        else:
            super().save_model(request, obj, form, change)
            if change:
                messages.success(request, f"Mehmonxona '{obj.name}' muvaffaqiyatli yangilandi!")
            else:
                messages.success(request, f"Mehmonxona '{obj.name}' muvaffaqiyatli yaratildi!")


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['room_no', 'hotel', 'room_type', 'rate', 'is_available', 'no_of_beds']

    def save_model(self, request, obj, form, change):
        if not change and Room.objects.filter(room_no=obj.room_no, hotel=obj.hotel).exists():
            messages.error(request, f"Xona {obj.room_no} '{obj.hotel.name}' mehmonxonasida allaqachon mavjud!")
        else:
            super().save_model(request, obj, form, change)
            if change:
                messages.success(request, f"Xona {obj.room_no} muvaffaqiyatli yangilandi!")
            else:
                messages.success(request, f"Xona {obj.room_no} muvaffaqiyatli yaratildi!")

@admin.register(Guest)
class GuestAdmin(admin.ModelAdmin):
    list_display = ['name', 'age', 'phone']

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['guest', 'room', 'hotel', 'checkin_date', 'checkout_date', 'check_out', 'no_of_guests']