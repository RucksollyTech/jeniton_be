from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import exceptions
from rest_framework.decorators import api_view,parser_classes
import datetime
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password

from rest_framework import status

from .models import Images,Profile,CityData,USerToken,Reviews,Purchases,Items,Items_Purchases,Newsletter
from .serializers import ProfileDetailSerializer,Location_Data_Serializer,ItemsSerializer,ReviewsSerializer,USerSerializer

from .authentication import decode_refresh_token,JWTAuthentication,create_access_token,create_refresh_token,decode_access_token

from django.conf import settings
from django.db.models import Q

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import EmailMultiAlternatives

from decouple import config
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from jeniton.mail_sender import sender_func
# from jeniton.other_mails import other_mail

from django.contrib.auth.models import User


from rest_framework.parsers import MultiPartParser


@api_view(['GET'])
def home(request,*args,**kwargs):
    allData = Items.objects.all()
    all_data = ItemsSerializer(allData,many=True)
    context = {
        "all_data" : all_data.data,
    }
    return Response(context,status=200)

@api_view(['GET'])
def find_category(request,cat,*args,**kwargs):
    obj = Items.objects.filter(category__icontains=cat).all()
    serializers = ItemsSerializer(obj,many = True)
    return Response({"items":serializers.data},status=200)

@api_view(['GET'])
def item_detail(request,pk,*args,**kwargs):
    obj = Items.objects.get(pk=int(pk))
    serializers = ItemsSerializer(obj,context={"detail": True})
    similar_items = Items.objects.filter(name__icontains=obj.name,category__icontains=obj.category).exclude(id=obj.id).all()[:6]
    serializer_similar_items = ItemsSerializer(similar_items,many=True)
    return Response({"data":serializers.data,"similar":serializer_similar_items.data},status=200)

@api_view(['GET'])
def item_review_data(request,pk,*args,**kwargs):
    obj = Items.objects.get(pk=int(pk))
    serializer = ReviewsSerializer(obj.reviews,many=True)
    return Response(serializer.data,status=200)

@api_view(['GET'])
def all_items(request,*args,**kwargs):
    obj = Items.objects.all()
    serializers = ItemsSerializer(obj, many = True)
    return Response({"items":serializers.data},status=200)

@api_view(['GET'])
def delivery_location_data(request,*args,**kwargs):
    obj = CityData.objects.get(pk=1)
    serializers = Location_Data_Serializer(obj)
    return Response(serializers.data,status=200)

@api_view(['POST'])
def update_cart(request,*args,**kwargs):
    ids = request.data.get('ids')
    obj = Items.objects.filter(id__in=ids).all()
    serializers = ItemsSerializer(obj, many = True)
    return Response(serializers.data,status=200)

@api_view(['POST'])
def make_reviews(request,*args,**kwargs):
    pk = request.data.get('id')
    rate = request.data.get('rate')
    review = request.data.get('review')

    obj = Items.objects.get(pk=int(pk))
    rev = Reviews.objects.create(review=review, value=rate)
    if obj:
        obj.reviews.add(rev)
    serializer = ReviewsSerializer(rev)
    serializers = ReviewsSerializer(obj.reviews.all()[:4],many=True)
    return Response({"review":serializer.data,"reviews":serializers.data},status=200)

@api_view(['GET'])
def default_search(request,*args,**kwargs):
    popular = Items.objects.order_by('-popular').all()[:10]
    all_new = Items.objects.order_by('-id').all()[:10]
    luxurious = Items.objects.order_by('-price').all()[:10]
    context= {
        "popular": ItemsSerializer(popular,many = True).data,
        "allNew" : ItemsSerializer(all_new,many = True).data,
        "luxurious" : ItemsSerializer(luxurious,many = True).data,
    }
    return Response(context,status=200)

# @api_view(['POST'])
# def search(request,*args,**kwargs):
#     query = request.data.get('search')
#     if query:
#         items = Items.objects.filter(
#             Q(name__icontains=query) | 
#             Q(category__icontains=query) | 
#             Q(sizes__icontains=query) |  
#             Q(color__icontains=query) |  
#             Q(price__icontains=query)  
#         )
#         # items_data = list(items.values('id', 'name', 'categories', 'sizes', 'price'))
#         results= ItemsSerializer(items,many = True).data
#         return Response({"items":results},status=200)
#     else:
#         return Response([],status=404)

class RegisterApiViews(APIView):
    def post(self, request):
        data = request.data
        if data["password"] != data["password_confirm"]:
            raise exceptions.APIException("Passwords do not match")
        
        user = User.objects.create(
            first_name=data['first_name'],
            last_name=data["last_name"],
            username=data['email'],
            email=data['email']
        )
        user.set_password(data['password'])
        user.save()
        access_token =  create_access_token(user.id)
        refresh_token = create_refresh_token(user.id)
        USerToken.objects.create(user_id=user.id, token=refresh_token, expired_at=datetime.datetime.utcnow() + datetime.timedelta(days=7))
        # response = JsonResponse({"token": access_token, "user": USerSerializer(user).data})

        # response.set_cookie(key="refresh_token", value=refresh_token, httponly=True)

        response = Response()
        response.status = 200
        response.set_cookie(key="refresh_token",value=refresh_token,httponly=True)
        response.data ={
            "token" : access_token,
            "refresh_token" : refresh_token,
            "user" : USerSerializer(user).data
        }
        return response


class LoginAPIView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = User.objects.filter(email=email).first()
        if not user:
            raise exceptions.AuthenticationFailed("Invalid credentials")
        if not user.check_password(password):
            raise exceptions.AuthenticationFailed("Invalid credentials")
        access_token =  create_access_token(user.id)
        refresh_token = create_refresh_token(user.id)
        USerToken.objects.create(user_id=user.id, token=refresh_token, expired_at=datetime.datetime.utcnow() + datetime.timedelta(days=7))
        response = Response()
        response.set_cookie(key="refresh_token",value=refresh_token,httponly=True)
        # response.data ={
        #     "token" : access_token
        # }
        response.data ={
            "token" : access_token,
            "refresh_token" : refresh_token,
            "user" : USerSerializer(user).data
        }
        return response

class UserAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    def get(self,request):
        serializer = USerSerializer(request.user)
        return Response({"user":serializer.data},status=200)

class RefreshAPIView(APIView):
    def post(self,request):
        refresh_token = request.data.get('refresh_token')
        # refresh_token = request.COOKIES.get('refresh_token')
        _id = decode_refresh_token(refresh_token)
        if not USerToken.objects.filter(user_id=_id,token=refresh_token,expired_at__gt=datetime.datetime.now(tz=datetime.timezone.utc)).exists():
            raise exceptions.AuthenticationFailed("Invalid token")
        access_token = create_access_token(_id)
        user = User.objects.get(pk=_id)
        serializer = USerSerializer(user)
        return Response({
            "token" : access_token,
            "user" : serializer.data,
        })

class LogoutAPIView(APIView):
    def post(self,request):
        # refresh_token = request.COOKIES.get("refresh_token")
        refresh_token = request.data.get("data")
        USerToken.objects.filter(token=refresh_token).delete()
        response = Response()
        response.delete_cookie(key="refresh_token")
        response.data= {
            "message":"success",
        }
        response.status= 200
        return response

@api_view(['POST'])
def search(request,*args,**kwargs):
    page = request.query_params.get("page")
    search = request.query_params.get("search")
    query = request.query_params.get("value")
    items =[]
    if search:
        items = Items.objects.filter(
            Q(name__icontains=search) | 
            Q(category__icontains=search) | 
            Q(sizes__icontains=search) |  
            Q(color__icontains=search) |  
            Q(price__icontains=search)  
        )
    if query:
        if query == "popular":
            items = Items.objects.order_by('-popular').all()
        if query == "luxurious":
            items = Items.objects.order_by('-price').all()
        if query == "all_new":
            items = Items.objects.order_by('-id').all()

    paginator = Paginator(items,20)
    
    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        page = paginator.num_pages
        items = paginator.page(paginator.num_pages)
    serializer = ItemsSerializer(items,many=True)
    if page == None:
        page = 1
    page = int(page) 
    context={
        "items" : serializer.data,
        "page": page, 
        "pages": paginator.num_pages
    }
    return Response(context,status=200)


@api_view(['POST'])
def reset_request(request,*args,**kwargs):
    email = request.data.get["email"]
    # email = request.data
    user = User.objects.filter(email=email).first()
    if not user:
        raise exceptions.ValidationError("Bad request")
    profile= Profile.objects.filter(user=user).first()
    send_reset_password_email(profile)
    return Response({"success":"success"},status=200)


@api_view(['GET','POST'])
def reset_token(request,*args,**kwargs):
    
    data = request.data
    user = Profile.verify_reset_token(data["token"])
    if user is None:
        message = {'detail': 'That is invalid or expired token. Please request reset password again'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
    if not data:
        message = {'detail': 'An Error occurred'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
    user.password=make_password(data['password'])
    user.save()
    return Response({"success":"success"},status=201)



def send_reset_password_email(user):
    token = user.get_reset_token()
    user= user.user
    html_massage= f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta http-equiv="X-UA-Compatible" content="IE=edge">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Reset password</title>
        </head>
        <body style="background-color: #F4F4F4; margin: 0; font-family: Arial;">
            <div style="text-align: center;">
                <img style="max-width: 50px;" src="{config('FRONTEND_URL')}/Images/kids multicultural logo 2.png" alt="">
            </div>
            <div style="display: flex;align-items: center; ">
                <div style=" margin: 30px auto;max-width: 650px;width: 100%;position: relative;">
                    <div style="background-color: #fff;border-radius: 0 0 10px 10px ;">
                        <div style="background-color: #1A5FFF;padding: 1.5px;"></div>
                        <div style="padding: 0 10px 10px 10px;">
                            <div style="padding-top: 25px; font-size:15px; text-align: center;">
                                To reset your password click on the button bellow:
                            </div>
                            <div style="padding: 30px 0 40px 0; font-size:15px;text-align: center;border-bottom: 1px solid #f1f1f1;">
                                <a href="{settings.FRONTEND_URL}/reset-password/{token}" style="padding:8px 20px; background-color: #1A5FFF;text-decoration:none;color:#fff;border-radius: 3px;font-size: 14px;">Reset password</a>
                            </div>
                            <div style="padding-top: 30px; font-size:15px;text-align: center;">
                                Or copy and paste the following link into your browser url {settings.FRONTEND_URL}/reset-password/{token}
                            </div>
                            <div style="padding-top: 25px; font-size:15px;text-align: center;">
                                Please note that this link is only valid for 10 minutes.
                            </div>
                            <div style="padding-top: 30px; font-size:15px;text-align: center;">
                                If you are unaware of this request, simply ignore this email and no changes will be made to your account.
                            </div>
                            
                        </div>
                    </div>
                    <div style="text-align: center;padding-top: 20px;">
                        <a style="color: transparent;" href="https://www.instagram.com/invites/contact/?i=r9f4juooz429&utm_content=9adyr3e">
                            <img style="margin-right: 10px;" width="35" height="35" src="https://img.icons8.com/ios-glyphs/35/BABABA/instagram-new.png" alt="instagram-new"/>
                        </a>
                        <a style="color: transparent;" href="https://www.facebook.com/chicagokidsmulticulturalfashionshow?mibextid=LQQJ4d">
                            <img width="35" height="35" src="https://img.icons8.com/ios-filled/35/BABABA/facebook-new.png" alt="facebook-new"/>
                        </a>
                    </div>
                    <span style="
                        padding: 15px;
                        font-size: 11px;
                        color: #6C757D;
                        display: block;
                        text-align: center;
                        font-weight: 500;
                    ">
                        You received this email to let you know about important changes 
                        to your Kids Multicultural World account.
                        © 2023 Kids Multicultural World, PO BOX :
                        90042 Henderson NV, 89009, USA
                    </span>
                </div>
            </div>
        </body>
        </html>
    """
    subject, to = 'Reset password', user.email
    text_content = ''
    form_email = "kryspatra.services@gmail.com"
    msg = EmailMultiAlternatives(subject, text_content,form_email, [to])
    msg.attach_alternative(html_massage, "text/html")
    msg.send(fail_silently=False)
    

class add_items_view(APIView):
    authentication_classes = [JWTAuthentication]
    def post(self,request):
        data = request.data
        
        if not data:
            message = {'error': 'Invalid request'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
        obj = Items.objects.create(
            user = request.user,
            name=data.get('name'),
            category=data.get('category'),
            price=data.get('price'),
            cover_image=request.FILES.get('image'),
        )
        if request.FILES.getlist('files'):
            for file in request.FILES.getlist('files'):
                img = Images.objects.create(image=file)
                obj.other_images.add(img)
        if data.get('description'):
            obj.description = data.get('description')
            obj.save()
        if data.get('material'):
            obj.material = data.get('material')
            obj.save()
        if data.get('sustainability'):
            obj.sustainability = data.get('sustainability')
            obj.save()
        if data.get('product_care'):
            obj.product_care = data.get('product_care')
            obj.save()
        if data.get('extra_information'):
            obj.extra_information = data.get('extra_information')
            obj.save()
        if data.get('color'):
            obj.color = data.get('color')
            obj.save()
        if data.get('amount_available'):
            obj.amount_available = data.get('amount_available')
            obj.save()
        if data.get('sizes_value_measurement'):
            obj.sizes_value_measurement = data.get('sizes_value_measurement')
            obj.save()
        if data.get('dimensions_LHW_in_inches'):
            obj.dimensions_LHW_in_inches = data.get('dimensions_LHW_in_inches')
            obj.save()
        if data.get('sizes'):
            obj.sizes = data.get('sizes')
            obj.save()
        if data.get('properties'):
            obj.properties_separated_with_double_comma = data.get('properties')
            obj.save()
        return Response({"id":obj.id},status=200)


class add_kyc_passport_image(APIView):
    authentication_classes = [JWTAuthentication]
    parser_classes = [MultiPartParser]

    def post(self, request):
        file1 = request.FILES['file']
        if not file1:
            return JsonResponse({"error": "Invalid request"}, status=400)
        try:
            profile, _ = Profile.objects.get_or_create(user=request.user)
            profile.passport_photo = file1
            profile.save()
            serializer = ProfileDetailSerializer(profile)
            return Response(serializer.data, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

class add_kyc_id_image(APIView):
    parser_classes = [MultiPartParser]
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        file1 = request.FILES.get('image')
        if not file1:
            return JsonResponse({"error": "Both images are required"}, status=400)
        profile = Profile.objects.filter(request.user)
        if not profile:
            profile = Profile.create(user=request.user)
        profile.passport_photo = file1
        profile.save()
        serializers = ProfileDetailSerializer(profile, many = True)
        return Response(serializers.data,status=200)

class add_kyc_bio(APIView):
    parser_classes = [MultiPartParser]
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        data = request.data
        if not data:
            return JsonResponse({"error": "Both images are required"}, status=400)
        try:
            profile, _ = Profile.objects.get_or_create(user=request.user)
            profile.country = data.get("country")
            profile.address = data.get("address")
            profile.state = data.get("state")
            profile.city = data.get("city")
            profile.bio = True

            profile.save()
            serializer = ProfileDetailSerializer(profile)
            return Response(serializer.data, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)


class GetProfile(APIView):
    authentication_classes = [JWTAuthentication]
    def get(self, request):
        profile, _ = Profile.objects.get_or_create(user=request.user)
        serializer = ProfileDetailSerializer(profile)
        return Response(serializer.data, status=200)


@api_view(['GET'])
def edit_items_view(request,pk,*args,**kwargs):
    data = request.data
    obj = Items.objects.filter(id__in=pk).all()
    serializers = ItemsSerializer(obj, many = True)
    return Response(serializers.data,status=200)



@api_view(['POST'])
def newsletter(request,*args,**kwargs):
    data = request.data
    data_check = Newsletter.objects.filter(email=data.get('email')).first()
    if not data_check:
        Newsletter.objects.create(
            email = data.get('email'),
        )
        the_mail = f'''
            <p>Your newsletter subscription was successful.</p>
            <p style="padding-top:30px">Click the button below unsubscribe anytime.</p>
            <p>
                <a
                    href="{settings.FRONTEND_URL}/unsubscribe/{data.get('email')}"
                    style="background:black; color: #fff; 
                    padding: 8px 20px;border:none;
                    text-decoration:none; border-radius: 10px"
                >
                    Unsubscribe
                </a>
            </p>
        '''
        other_mail(data.get('email'),the_mail)
    return Response("success",status=200)

@api_view(['POST'])
def unsubscribe(request,*args,**kwargs):
    data = request.data
    data_check = Newsletter.objects.filter(email=data.get('email')).first()
    if data_check:
        data_check.delete()
        the_mail = f'''
            <p>Your request to unsubscribe for newsletter was successful.</p>
        '''
        other_mail(data.get('email'),the_mail)
    return Response("success",status=200)



# def calculate_Price(x):
#     price = 0
#     for i in x:
#         item_price = Items.objects.get(pk=int(i["id"]))
#         price = price + (item_price.price * int(i["counter"]))
#     return (price + 6)


# def thePaymentHandler(product,price):
#     try:
#         intent = stripe.PaymentIntent.create(
#             amount=int(price) * 100,
#             currency='usd',
#             automatic_payment_methods={
#                 'enabled': True,
#             },
#             metadata={
#                 "product_id": f"item{product.id}"
#             }
#         )
#         return [True,intent]
#     except Exception as e:
#         return [False,str(e)]



# def getItems(items) :
#     ff = ""
#     try :
#         for i in items:
#             ff = ff + f'''<li><a href="{settings.FRONTEND_URL}/item_detail/{i.id}">Number of item:{i.counter}, Name :{i.name}</a></li>'''
#     except:
#         pass
#     return f'<ol>{ff}</ol>'

# def purchase_email(
#     email,
#     user_name,
#     price,
#     phone,
#     address,
#     items
#     ):

    

#     html_massage= f"""
#         <body style="background-color: #F4F4F4; margin: 0;overflow-x: hidden; font-family: Arial;">
#             <div style="display: flex;align-items: center; ">
#                 <div style=" margin: 30px auto;max-width: 650px;width: 100%;position: relative;">
#                     <div style="background-color: #fff;border-radius: 0 0 10px 10px ;">
#                         <div style="background-color: #1A5FFF;padding: 1.5px;"></div>
#                         <div style="padding: 0 10px 10px 10px;">
#                             <div style="padding-top: 25px; font-size:15px;text-align: center;">
#                                 Customer Name : {user_name}
#                             </div>
#                             <div style="padding-top: 25px; font-size:15px;text-align: center;">
#                                 Price : {price}
#                             </div>
#                             <div style="padding-top: 25px; font-size:15px;text-align: center;">
#                                 Customer Email : {email}
#                             </div>
#                             <div style="padding-top: 25px; font-size:15px;text-align: center;">
#                                 Customer Phone : {phone}
#                             </div>
#                             <div style="padding-top: 25px; font-size:15px;text-align: center;">
#                                 Customer Address : {address}
#                             </div>
#                             <div style="padding-top: 25px; font-size:15px;text-align: center;">
#                                 Items Purchased : {getItems(items)}
#                             </div>
                            
#                         </div>
#                     </div>
#                 </div>
#             </div>
#         </body>
#         </html>
#     """
#     subject, to = "Payment Information", email
#     text_content = ''
#     form_email = settings.ADMIN_EMAIL_ADDRESSS
#     msg = EmailMultiAlternatives(subject, text_content,form_email, [to])
#     msg.attach_alternative(html_massage, "text/html")
#     msg.send(fail_silently=True)



# @api_view(['GET','POST'])
# def CreatePaymentIntent(request,*args,**kwargs):
#     prod_id = request.data
#     daProduct = prod_id.get("items")
#     def check (product, price):
#         inten = thePaymentHandler(product,price)
        
#         if inten[0] == True:
#             intent = inten[1]
#             prod = Purchases.objects.get(pk = product.id)
#             prod.reference = intent['client_secret']
#             prod.save()
#             return Response({
#                 'clientSecret': intent['client_secret']
#             },status=200)

#         else:
#             intent = inten[1]
#             return Response(intent,status=403)

#     if prod_id.get("type") == "cart" and int(daProduct["price"]) == calculate_Price(daProduct["item"]):
        
#         product = Purchases.objects.create(
#             email = daProduct["email"],
#             name = daProduct["name"],
#             users_address=daProduct["users_address"],
#             country = daProduct["country"],
#             city = daProduct["city"],
#             zipcode = daProduct["zipcode"],
#             price= int(daProduct["price"]),
#             # apartment = daProduct["apartment"],
#             counter = daProduct["counter"],
#             phone=daProduct["phone"],
#             state = daProduct["state"],
#         )
#         product.purchase_id =product.id + 1897
#         product.save()

#         for i in daProduct["item"]:
#             bg = Items.objects.get(pk=int(i["id"]))
#             bg_created = Items_Purchases.objects.create(
#                 item = bg,
#                 email = product.email,
#                 counter = i["counter"]
#             )
#             product.item.add(bg_created)
#         product.save()
#         dat = check(product,prod_id.get("items")["price"])
#         return dat
#     if prod_id.get("type") == "track":
#         product = Purchases.objects.filter(reference=prod_id.get("secrete")).first()
#         if product:
#             product.success = True
#             product.save()
#             try:
#                 thData = {
#                     "title" : "Successful Payment Confirmation",
#                     "receipt" : True,
#                     "id": product.purchase_id,
#                     "item": getItems(product.item),
#                     "counter": product.counter,
#                     "price" : product.price
#                 }
#                 sender_func(product.email,thData)
#                 purchase_email(
#                     settings.ADMIN_EMAIL_ADDRESSS,
#                     product.name,
#                     product.price,
#                     product.phone,
#                     product.address,
#                     product.item
#                 )
#             except:
#                 pass
#             return Response("success",status=200)
    
#     return Response("error",status=403)


