from django.contrib import admin

# Register your models here.

from .models import Images,Items,Purchases,Newsletter


admin.site.register(Images)
admin.site.register(Items)
admin.site.register(Purchases)
admin.site.register(Newsletter)