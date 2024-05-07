
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from jeniton.views import delivery_location_data,update_cart,LogoutAPIView,RefreshAPIView,UserAPIView,LoginAPIView,RegisterApiViews,home,find_category,make_reviews,unsubscribe,item_review_data,item_detail,all_items,items_search,newsletter
 #,CreatePaymentIntent

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/home', home),
    path('api/items', all_items),
    # path('api/checkout', CreatePaymentIntent),
    path('api/newsletter', newsletter),
    path('api/unsubscribe', unsubscribe),
    path('api/write_reviews', make_reviews),
    path('api/search', items_search),
    path('api/update-cart', update_cart),
    path('api/location-data', delivery_location_data),
    path('api/register', RegisterApiViews.as_view()),
    path('api/login', LoginAPIView.as_view()),
    path('api/user', UserAPIView.as_view()),
    path('api/refresh', RefreshAPIView.as_view()),
    path('api/logout', LogoutAPIView.as_view()),
    path('api/items_category/<str:cat>', find_category),
    path('api/item_detail/<str:pk>', item_detail),
    path('api/item_review/<str:pk>', item_review_data),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

