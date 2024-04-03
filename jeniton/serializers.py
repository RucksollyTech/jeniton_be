from rest_framework import serializers
from .models import Purchases,Items,Images,Items_Purchases
from django.contrib.auth.models import User
# from rest_framework_simplejwt.tokens import RefreshToken


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = ['id', 'image']

class Items_PurchasesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Items_Purchases
        fields = '__all__'

class PurchasesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchases
        fields = '__all__'

class ItemsSerializer(serializers.ModelSerializer):
    other_images = serializers.SerializerMethodField(read_only= True)
    class Meta:
        model = Items
        fields = ['id', 'name','color','price','cover_image','description','dimensions_LHW_in_inches','properties_separated_with_double_comma','extra_information','sustainability','product_care','material','other_images','amount_available','model_image','date']

    def get_other_images(self,obj):
        return ImageSerializer(obj.other_images, many=True).data















