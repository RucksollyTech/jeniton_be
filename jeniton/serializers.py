from rest_framework import serializers
from .models import Profile,Reviews,Purchases,Items,Images,Items_Purchases,CityData
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

class Location_Data_Serializer(serializers.ModelSerializer):
    class Meta:
        model = CityData
        fields = '__all__'

class PurchasesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchases
        fields = '__all__'

class ReviewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reviews
        fields = '__all__'


class ItemsSerializer(serializers.ModelSerializer):
    other_images = serializers.SerializerMethodField(read_only= True)
    reviews = serializers.SerializerMethodField(read_only= True)
    
    properties = serializers.SerializerMethodField(read_only= True)
    class Meta:
        model = Items
        fields = ['id', 'name','is_sold_out','color','category','sizes','sizes_value_measurement','material','price','cover_image','reviews','description','dimensions_LHW_in_inches','properties','extra_information','sustainability','product_care','other_images','amount_available','date']

    def get_other_images(self,obj):
        return ImageSerializer(obj.other_images, many=True).data
    def get_properties(self,obj):
        if not obj.properties_separated_with_double_comma:
            return ""
        if obj.properties_separated_with_double_comma:
            return obj.properties_separated_with_double_comma
        return ""
    def get_reviews(self,obj):
        is_for_detail = self.context.get("detail")
        return ReviewsSerializer(obj.reviews.all()[:4] if is_for_detail else obj.reviews, many=True).data


class USerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
        extra_kwargs = {'password': {'write_only': True}}
        def create(self, validated_data):
            password = validated_data.pop('password', None)
            instance = self.Meta.model(**validated_data)
            if password is not None:
                instance.set_password(password)
            instance.save()
            return instance



class ProfileDetailSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(read_only= True)
    complete_id = serializers.SerializerMethodField(read_only= True)
    id_photo1 = serializers.SerializerMethodField(read_only= True)
    id_photo2 = serializers.SerializerMethodField(read_only= True)
    passport_photo = serializers.SerializerMethodField(read_only= True)
    class Meta:
        model = Profile
        fields = [
            # "user",
            "phone","profile_photo",
            "attempt_verification","is_verified",
            "id_type","id_photo1","id_photo2",
            "passport_photo","bio","complete_id",
            "name","date"
        ]
    def get_name(self,obj):
        return f"{obj.user.first_name} {obj.user.last_name}"
    def get_complete_id(self,obj):
        if obj.id_type == "International passport":
            return True if obj.id_photo1 else False
        return True if (obj.id_photo1 and obj.id_photo2) else False
    def get_id_photo1(self,obj):
        return True if obj.id_photo1 else False
    def get_id_photo2(self,obj):
        return True if obj.id_photo2 else False
    
    def get_passport_photo(self,obj):
        return True if obj.passport_photo else False











