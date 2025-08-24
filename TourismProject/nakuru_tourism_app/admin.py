from django.contrib import admin
from .models import CustomUser, Attraction, Category, Rating

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Attraction)
admin.site.register(Category)
admin.site.register(Rating)
