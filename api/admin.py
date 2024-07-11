from django.contrib import admin
from .models import Arma

# Register your models here.
class ArmasAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_item_name', 'precio','stickers_custom')
    search_fields = ('full_item_name',)
    list_editable = ('precio',)
    # list_per_page = 20


admin.site.register(Arma,ArmasAdmin)