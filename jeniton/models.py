from django.db import models
from django.db.models.signals import post_save
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from django.conf import settings
from jeniton.mail_sender import sender_func
from django.contrib.auth.models import User as User2
import random
User = settings.AUTH_USER_MODEL

def generate_unique_id(k):
    unique_id = ''.join(random.choices('0123456789', k=k))
    return unique_id


class USerToken(models.Model):
    user_id = models.IntegerField()
    token = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    expired_at = models.DateTimeField()
    date= models.DateTimeField(auto_now_add = True)


class Images(models.Model):
    image = models.ImageField(upload_to ="media/", null=True,blank=True)
    date= models.DateTimeField(auto_now_add = True)
    
    class Meta:
        ordering= ["-id"]
        
    def __str__(self):
        return f"image--{self.image}"

class Reviews(models.Model):
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True) 
    review = models.TextField( null=True,blank=True)
    value = models.IntegerField(default =0)
    date= models.DateTimeField(auto_now_add = True)
    
    class Meta:
        ordering= ["-id"]
        
    def __str__(self):
        return f"Review--{self.value}"

class Notifications(models.Model):
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True) 
    viewed = models.BooleanField(default=True)
    priority = models.IntegerField(default =0)
    title = models.CharField(max_length=255, null= True , blank=True)
    content = models.TextField(null= True, blank=True)
    order_id= models.IntegerField(null= True, blank=True)
    date= models.DateTimeField(auto_now_add = True)
    
    class Meta:
        ordering= ["-id"]

class CityData(models.Model):
    data = models.JSONField()
    stat_and_price = models.JSONField(null=True,blank=True)
    date= models.DateTimeField(auto_now_add = True)
    
    def __str__(self):
        return f"City data {self.id}"

class Items(models.Model):
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True) 
    name = models.CharField(max_length=1000)
    color = models.CharField(max_length=1000, null=True,blank=True) 
    category = models.CharField(max_length=1000, null=True,blank=True,default="Bag,Shoe or Hair") 
    material = models.CharField(max_length=1000, null=True,blank=True) 
    price = models.IntegerField(default =0)
    popular = models.IntegerField(default =0)
    cover_image = models.ImageField(upload_to ="media/", null=True,blank=True)
    other_images = models.ManyToManyField(Images,blank=True)
    reviews = models.ManyToManyField(Reviews,blank=True)
    amount_available = models.IntegerField(default =-2000)
    sizes = models.CharField(max_length=1000, null=True,blank=True) 
    sizes_value_measurement = models.CharField(max_length=1000, null=True,blank=True,default="UK") 
    description = models.TextField( null=True,blank=True)
    is_sold_out = models.BooleanField(default=False)
    in_store = models.BooleanField(default=False)
    available = models.BooleanField(default=True)
    dimensions_LHW_in_inches = models.CharField(max_length=1000, null=True,blank=True,default="0 x 0 x 0")
    properties_separated_with_double_comma = models.TextField( null=True,blank=True,default="Ankara Item,,Durable")
    extra_information = models.TextField( null=True,blank=True)
    sustainability = models.TextField( null=True,blank=True)
    product_care = models.TextField( null=True,blank=True)
    counter = models.IntegerField(default =0)
    status =  models.CharField(max_length=8, null=True,blank=True,default="Available") #Finished
    date= models.DateTimeField(auto_now_add = True)
    
    class Meta:
        ordering= ["-id"]
        
    def __str__(self):
        return f"{self.name}"


class Orders(models.Model):
    owner = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True)
    user = models.ForeignKey(User,related_name="buyer",on_delete=models.SET_NULL,null=True,blank=True)
    item = models.ForeignKey(Items,on_delete=models.SET_NULL,null=True,blank=True)
    counter = models.IntegerField(default =1)
    price = models.IntegerField(default =0)
    color= models.CharField(max_length=10,null=True, blank=True)
    size = models.TextField(null=True, blank=True)
    available = models.BooleanField(default=True)
    drop_off_id = models.IntegerField(default =1)
    display_id = models.IntegerField(default =1)
    purchase_reference = models.CharField(max_length =20, blank = True, null=True)
    status =  models.CharField(max_length=20, null=True,blank=True,default="Not dispatched") #Dispatched 

    date= models.DateTimeField(auto_now_add = True)

    class Meta:
        ordering= ["-date"]
    
    def save(self, *args, **kwargs):
        if not self.drop_off_id :
            def get_id():
                random_id = 0
                def checker(id_field):
                    check_orders= Orders.objects.filter(drop_off_id = id_field)
                    return check_orders
                contiNue = True
                while contiNue:
                    random_id = generate_unique_id(11)
                    if not checker(random_id):
                        contiNue = False
                return random_id

            random_id = get_id()
            self.drop_off_id = random_id
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.drop_off_id}"


class Purchases(models.Model):
    name = models.CharField(max_length=1000,null=True,blank=True)
    # To determine is for seller or customer
    bought = models.BooleanField(default=False)
    email = models.CharField(max_length=1000,null=True,blank=True)
    users_address = models.CharField(max_length=1000,null=True,blank=True)
    country= models.CharField(max_length=1000,null=True,blank=True)
    city = models.CharField(max_length=1000,null=True,blank=True)
    state = models.CharField(max_length=1000,default="USA")
    zipcode = models.CharField(max_length=1000,null=True,blank=True)
    phone= models.CharField(max_length=1000,null=True,blank=True)
    price = models.IntegerField(default =0)
    order_id = models.IntegerField(default =0)
    apartment = models.CharField(max_length=1000,null=True,blank=True)
    item = models.ManyToManyField(Orders,blank=True) 
    counter = models.IntegerField(default =1)
    delivered = models.BooleanField(default=False)
    received = models.BooleanField(default=False)
    dont_touch_this_for_system_use_only = models.BooleanField(default=False)
    reference = models.CharField(max_length=20,null=True,blank=True)
    date= models.DateTimeField(auto_now_add = True)
    
    class Meta:
        ordering= ["-date"]
    
    def save(self, *args, **kwargs):
        if self.delivered == True and self.dont_touch_this_for_system_use_only == False:
            thData = {
                "title" : "Order Delivery Confirmation",
                "receipt" : False,
                "price": self.price,
                "counter": self.counter,
                "id": self.purchase_id
            }
            self.dont_touch_this_for_system_use_only = True
            sender_func(self.email,thData)
        def get_id():
            random_id = generate_unique_id(12)
            def checker(id_field):
                check_orders= Purchases.objects.filter(order_id = id_field)
                return check_orders
            contiNue = True
            while contiNue:
                random_id = generate_unique_id(6)
                if not checker(random_id):
                    contiNue = False
            return random_id
        random_id = get_id()
        self.order_id = random_id
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.order_id}"
    

class Newsletter(models.Model):
    email = models.TextField( null=True,blank=True)
    date= models.DateTimeField(auto_now_add = True)
    
    class Meta:
        ordering= ["-id"]
        
    def __str__(self):
        return f"{self.email}"



class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    phone = models.CharField(max_length=200,null=True,blank=True)
    profile_photo = models.ImageField(upload_to ="media/", null=True,blank=True)
    passport_photo = models.ImageField(upload_to ="media/", null=True,blank=True)
    id_photo1 = models.ImageField(upload_to ="media/", null=True,blank=True)
    id_photo2 = models.ImageField(upload_to ="media/", null=True,blank=True)
    ballance = models.IntegerField(default =0)
    # other_images = models.ManyToManyField(Images,blank=True)
    id_type = models.CharField(max_length=50,null=True,blank=True)
    country = models.CharField(max_length=200,null=True,blank=True)
    is_verified = models.BooleanField(default=False)
    bio = models.BooleanField(default=False)
    attempt_verification = models.BooleanField(default=False)
    address = models.TextField(null=True,blank=True)
    state = models.TextField(null=True,blank=True)
    city = models.TextField(null=True,blank=True)

    date= models.DateTimeField(auto_now_add = True)
    
    
    def get_reset_token(self, expires_sec=600):
        s = Serializer(settings.SECRET_KEY, expires_sec)
        return s.dumps({'user_id': self.user.id}).decode('utf-8')


    @staticmethod
    def verify_reset_token(token):
        s = Serializer(settings.SECRET_KEY)
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User2.objects.get(pk=user_id)
    
    def __str__(self):
        return self.user.email


def user_did_save(sender, instance, created, *args, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance)
post_save.connect(user_did_save, sender=User)
