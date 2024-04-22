from django.db import models
from django.conf import settings
from jeniton.mail_sender import sender_func
User = settings.AUTH_USER_MODEL

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


class Items(models.Model):
    name = models.CharField(max_length=1000)
    color = models.CharField(max_length=1000, null=True,blank=True) 
    category = models.CharField(max_length=1000, null=True,blank=True,default="Bag,Shoe or Hair") 
    material = models.CharField(max_length=1000, null=True,blank=True) 
    price = models.IntegerField(default =0)
    cover_image = models.ImageField(upload_to ="media/", null=True,blank=True)
    other_images = models.ManyToManyField(Images,blank=True)
    reviews = models.ManyToManyField(Reviews,blank=True)
    amount_available = models.IntegerField(default =0)
    sizes = models.CharField(max_length=1000, null=True,blank=True) 
    sizes_value_measurement = models.CharField(max_length=1000, null=True,blank=True,default="UK") 
    description = models.TextField( null=True,blank=True)
    dimensions_LHW_in_inches = models.CharField(max_length=1000, null=True,blank=True,default="0 x 0 x 0")
    properties_separated_with_double_comma = models.TextField( null=True,blank=True,default="Ankara Item,,Durable")
    extra_information = models.TextField( null=True,blank=True)
    sustainability = models.TextField( null=True,blank=True)
    product_care = models.TextField( null=True,blank=True)
    counter = models.IntegerField(default =0)
    date= models.DateTimeField(auto_now_add = True)
    
    class Meta:
        ordering= ["-id"]
        
    def __str__(self):
        return f"{self.name}"


class Items_Purchases(models.Model):
    item = models.ForeignKey(Items,on_delete=models.SET_NULL,null=True,blank=True) 
    email = models.CharField(max_length=1000)
    counter = models.IntegerField(default =1)
    date= models.DateTimeField(auto_now_add = True)

    class Meta:
        ordering= ["-date"]

    def __str__(self):
        return f"{self.email}"


class Purchases(models.Model):
    name = models.CharField(max_length=1000,null=True,blank=True)
    email = models.CharField(max_length=1000,null=True,blank=True)
    users_address = models.CharField(max_length=1000,null=True,blank=True)
    country= models.CharField(max_length=1000,null=True,blank=True)
    city = models.CharField(max_length=1000,null=True,blank=True)
    state = models.CharField(max_length=1000,default="USA")
    zipcode = models.CharField(max_length=1000,null=True,blank=True)
    phone= models.CharField(max_length=1000,null=True,blank=True)
    purchase_id = models.CharField(max_length=20, default=0)
    price = models.IntegerField(default =0)
    apartment = models.CharField(max_length=1000,null=True,blank=True)
    item = models.ManyToManyField(Items_Purchases,blank=True) 
    counter = models.IntegerField(default =1)
    success = models.BooleanField(default=False)
    delivered = models.BooleanField(default=False)
    dont_touch_this_for_system_use_only = models.BooleanField(default=False)
    reference = models.CharField(max_length=1000,null=True,blank=True)
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
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.purchase_id}--{self.email}--{'Delivered' if self.delivered else ''}"
    

class Newsletter(models.Model):
    email = models.TextField( null=True,blank=True)
    date= models.DateTimeField(auto_now_add = True)
    
    class Meta:
        ordering= ["-id"]
        
    def __str__(self):
        return f"{self.email}"


