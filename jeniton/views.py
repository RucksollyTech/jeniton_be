from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import get_authorization_header
from rest_framework import exceptions
from rest_framework.decorators import api_view,authentication_classes
import datetime
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password

from .models import CityData,USerToken,Reviews,Purchases,Items,Items_Purchases,Newsletter
from .serializers import Location_Data_Serializer,ItemsSerializer,ReviewsSerializer,USerSerializer

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










@api_view(['GET'])
def items_search(request,*args,**kwargs):
    page = request.query_params.get("page")
    query = request.query_params.get("query")
    items =[]
    if query:
        items = Items.objects.filter(Q(description__icontains=query)| Q(name__icontains=query)| Q(price__icontains=query)).all()
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


