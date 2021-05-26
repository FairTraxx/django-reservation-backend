from django.contrib import admin
from .models import Restaurant, Table, Booking

class RestaurantAdmin(admin.ModelAdmin):
    pass
admin.site.register(Restaurant, RestaurantAdmin)

class TableAdmin(admin.ModelAdmin):
    pass
admin.site.register(Table, RestaurantAdmin)

class BookingAdmin(admin.ModelAdmin):
    pass
admin.site.register(Booking, RestaurantAdmin)