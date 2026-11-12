from django.contrib import admin
from django.contrib.auth.models import Group
from .models import Brand, CarModel, Year, Listing, Profile, EmailVerification, CarModelBodyType, CarGeneration
admin.site.site_header = "Apex Administration"
admin.site.site_title = "Apex Admin Portal"
admin.site.index_title = "Welcome to Apex Management"

# Register your models here.




class CarModelBodyTypeInline(admin.TabularInline):
    model = CarModelBodyType
    extra = 1


class CarModelAdmin(admin.ModelAdmin):
    inlines = [CarModelBodyTypeInline]


admin.site.register(Brand)
admin.site.register(CarModel, CarModelAdmin)
admin.site.register(Year)
admin.site.register(Listing)
admin.site.register(Profile)
admin.site.register(EmailVerification)
admin.site.register(CarModelBodyType)
admin.site.register(CarGeneration)
admin.site.unregister(Group)

