from django.contrib import admin
from .models import * 
# Register your models here.

class RatingRestaurantInline(admin.TabularInline):
    model=Rating

class RestaurantAdmin(admin.ModelAdmin):
    inlines=[RatingRestaurantInline]


admin.site.register(User)
admin.site.register(OneTimePassword)
admin.site.register(UserProfile)

admin.site.register(Rating)
admin.site.register(Restaurant,RestaurantAdmin)
admin.site.register(Sale)
admin.site.register(Staff)
admin.site.register(StaffRestaurant)
