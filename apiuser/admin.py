from django.contrib import admin
from .models import * 
# Register your models here.
admin.site.register(User)
admin.site.register(OneTimePassword)

admin.site.register(Rating)
admin.site.register(Restaurant)
admin.site.register(Sale)
admin.site.register(Staff)
admin.site.register(StaffRestaurant)
