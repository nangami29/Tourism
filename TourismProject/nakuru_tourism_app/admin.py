from django.contrib import admin
from .models import CustomUser, Attraction, Category, Rating
from import_export.admin import ImportExportModelAdmin
# Register your models here.
admin.site.register(CustomUser)

admin.site.register(Category)
admin.site.register(Rating)
@admin.register(Attraction)
class AttractionAdmin(ImportExportModelAdmin):
    list_display = ('name', 'category', 'location', 'entry_fee')
    search_fields = ('name', 'category')