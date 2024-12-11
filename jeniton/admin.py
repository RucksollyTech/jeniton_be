from django.contrib import admin

# Register your models here.

from .models import Profile,Orders,CityData,Reviews,Images,Items,Purchases,Newsletter


admin.site.register(Images)
admin.site.register(Orders)
admin.site.register(CityData)
admin.site.register(Profile)
admin.site.register(Items)
admin.site.register(Reviews)
admin.site.register(Purchases)
admin.site.register(Newsletter)
