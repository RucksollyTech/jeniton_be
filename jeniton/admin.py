from django.contrib import admin

# Register your models here.

from .models import Reviews,Images,Items,Purchases,Newsletter


admin.site.register(Images)
admin.site.register(Items)
admin.site.register(Reviews)
admin.site.register(Purchases)
admin.site.register(Newsletter)
