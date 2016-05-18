from django.contrib import admin
from .models import *
from .forms import *
# Register your models here.

class ItemAdmin(admin.ModelAdmin):
	list_display = ('name', 'price', 'isveg')

class locationAdmin(admin.ModelAdmin):
	list_display = ('id', 'name')

class VendorLoginAdmin(admin.ModelAdmin):
	form = VendorLoginForm

class timeSlotAdmin(admin.ModelAdmin):
	list_display = ('start_time', 'end_time','max_limit')

admin.site.register(Item, ItemAdmin)
admin.site.register(Order)
admin.site.register(location,locationAdmin)
admin.site.register(timeSlot,timeSlotAdmin)
admin.site.register(Vendor)
admin.site.register(Genre)
admin.site.register(Feedback)
# admin.site.register(UserProfile)