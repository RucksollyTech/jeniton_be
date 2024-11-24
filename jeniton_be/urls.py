
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from jeniton.views import VerifyView,AllUserFinished,AllUserAvailable,EditItemsView,AllUserItems,add_profile_img,GetProfile,add_kyc_bio,add_kyc_id_image,add_kyc_passport_image,add_items_view,reset_token,reset_request,search,default_search,delivery_location_data,update_cart,LogoutAPIView,RefreshAPIView,UserAPIView,LoginAPIView,RegisterApiViews,home,find_category,make_reviews,unsubscribe,item_review_data,item_detail,all_items,newsletter
 #,CreatePaymentIntent

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/home', home),
    path('api/items', all_items),
    # path('api/checkout', CreatePaymentIntent),
    path('api/newsletter', newsletter),
    path('api/unsubscribe', unsubscribe),
    path('api/write_reviews', make_reviews),
    path('api/update-cart', update_cart),
    path('api/search', search),
    path('api/add_items', add_items_view.as_view()),
    # Kyc
    path('api/upload-kyc-data-passport-pix', add_kyc_passport_image.as_view()),
    path('api/upload-kyc-data-id-pix', add_kyc_id_image.as_view()), #here
    path('api/upload-kyc-data-bio', add_kyc_bio.as_view()),

    # profile add_profile_img
    path('api/get-profile', GetProfile.as_view()),
    path('api/set-profile-pix', add_profile_img.as_view()),

    # Checkout VerifyView
    path('api/verify_transaction', VerifyView.as_view()),
    
    path('api/forgot-password', reset_request),
    path('api/password-reset', reset_token),
    path('api/default/search', default_search),
    path('api/location-data', delivery_location_data),
    path('api/register', RegisterApiViews.as_view()),
    path('api/user-all-items', AllUserItems.as_view()),
    path('api/user-all-available', AllUserAvailable.as_view()),
    path('api/user-all-finished', AllUserFinished.as_view()),
    path('api/login', LoginAPIView.as_view()),
    path('api/user', UserAPIView.as_view()),
    path('api/refresh', RefreshAPIView.as_view()),
    path('api/logout', LogoutAPIView.as_view()),
    # path('api/edit_items/<str:pk>', edit_items_view),
    path('api/edit_items/<str:pk>', EditItemsView.as_view()),
    path('api/items_category/<str:cat>', find_category),
    path('api/item_detail/<str:pk>', item_detail),
    path('api/item_review/<str:pk>', item_review_data),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

