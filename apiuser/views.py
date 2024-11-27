from django.shortcuts import render , HttpResponse, redirect
from django.utils import timezone
from django.db.models import Q , Case ,When 
from django.db.models.functions import Lower,Upper,Length, Concat
from apiuser.serializers import *
# views.py
#from jwt.api.apiuser.serializers import *
from django.db .models import Max,Min, Avg,Sum, Count,CharField, Value
from apiuser.models import User
from django.db import connection
from rest_framework.generics import GenericAPIView
from .utils import send_code_to_user
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from django.utils.encoding import smart_str, DjangoUnicodeDecodeError
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from itertools import chain
from django_ratelimit.decorators import ratelimit
from django.utils.decorators import method_decorator
import logging
from django.http import JsonResponse

logger = logging.getLogger('django')
# Create your views here.
def home(request):
    return HttpResponse("jwt")

def run(request):
    rest1=Restaurant()
    #rest1.objects.delete
    restrecords=Restaurant.objects.get(id=1)
    rest=Restaurant.objects.first()
    #print(rest.sales.all())
    user=User.objects.first()
    #print(restrecords)

#     getcreate=Rating.objects.get_or_create(restaurant=rest,
#                                  user=user, rating=1
#                                  )
#     #print(getcreate)


    saledata= Sale.objects.filter(restaurant__restaurant_type=Restaurant.TypeChoices.INDIAN)
    print(saledata)

    salerecords=Sale.objects.filter(income__range=(3,4.5))
    print(salerecords.query)
    print([s.income for s in salerecords])

    restaurants=Restaurant.objects.prefetch_related('ratings')
    print(restaurants.query)

    for rest in restaurants:
        print(rest.name)
        for ratingrecords in rest.ratings.all():
            print(ratingrecords.rating)


    fivestarratings=Restaurant.objects.prefetch_related('ratings').filter(ratings__rating=5)
    print(fivestarratings)

    print(fivestarratings.query)

    staff,created=Staff.objects.get_or_create(name='John Doe')
    print(staff, created)

    #staff.restaurants.set(Restaurant.objects.all()[:3])
    #staff.restaurants.filter()

    staffrestaurant=Staff.objects.all()
    print(staff.restaurants.all())

    # StaffRestaurant.objects.create(staff=staff,restaurant=Restaurant.objects.first(),salary=28000)

    # StaffRestaurant.objects.create(staff=staff,restaurant=Restaurant.objects.last(),salary=25000)

    jobs=StaffRestaurant.objects.prefetch_related('restaurant','staff')

    for job in jobs:
        print(job.restaurant.name, job.restaurant.date_opened, job.salary)
        print(job.staff.name)



    # Sale.objects.create(restaurant=Restaurant.objects.first(),income=3.2,datetime=timezone.now())

    # print(restrecords.Rating_set.all())


    #print(connection.queries)
    # rest1.name="Italian Restaurant #1"
    # rest1.latitude=50.2
    # rest1.longitude=50.2
    # rest1.date_opened=timezone.now()
    # rest1.restaurant_type=Restaurant.TypeChoices.ITALIAN

    # rest1.save()


    return HttpResponse("yes")


def daterecords(request):
    one_month_ago=timezone.now()-timezone.timedelta(days=31)
    sales=Sale.objects.filter(datetime__gte=one_month_ago)
    # print(sales)
    # print(sales.aggregate(max=Max('income')))

    rests=Restaurant.objects.annotate(len_name=Length('name')).filter(
     len_name__gt=5  , len_name__lt=11   
    )
    # print(rests)
    # print(rests.query)

    concatenation=Concat('name',Value(' [Rating: '),Avg('ratings__rating'),Value(']'), output_field=CharField())

    restaurants=Restaurant.objects.annotate(message=concatenation)

    print(restaurants)

#     #print(restaurants.query)

    for r in restaurants:
        pass
        #print(r.message)

    sumsalesrestaurants=Restaurant.objects.aggregate(sum_sales=Count('sales'))

    sumsalesrestaurants=Restaurant.objects.annotate(salesrecord=Avg('sales__income'))
    print(sumsalesrestaurants.query)

    for i in sumsalesrestaurants:
        print(i,1)

    restgroupby= Restaurant.objects.values('restaurant_type').annotate(num_ratings=Count('ratings'))

    print(restgroupby)   
    print(restgroupby.query)  
               

    context={
            'restratings':restaurants,
            'restsales':sumsalesrestaurants

        }

    #print(sumsalesrestaurants)

    return render(request, "index.html",context)
    return HttpResponse(one_month_ago)


#permission using djnago classes.

class Restaurnat(APIView):
    # serializer_class = 
    permission_classes=[IsAuthenticated]

    @method_decorator(ratelimit(key='user', rate='5/d', method='GET', block=True))
    def get(self, request):
        logger.info("Restaurnat Endpoint  was hit")
        rest=Restaurant.objects.first()
        serializer = RestaurantSerializer(Restaurant.objects.all(), many=True)
        #serializerobject = RestaurantSerializer(rest, many=True)
        content = {
            'status': 'request was permitted',
            'data':  serializer.data
        }
        # logger.info("Restaurnat Endpoint  response  "{serializer.data})
        return Response(content)
    


#             serializer = UserRegisterSerializer(in_active_users, many=True)

#             return Response(serializer.data, status=status.HTTP_200_OK)

class RegisterView(GenericAPIView):
    serializer_class = UserRegisterSerializer

    def post(self, request):
        user = request.data
        print(request.data['first_name'],request.data['last_name'])
        if request.data['first_name']==request.data['last_name']:
             return Response({
                'data':request.data['first_name'],
                'message':'Both Firstname, lastname should not  be same'
            }, status=status.HTTP_201_CREATED)

        serializer=self.serializer_class(data=user)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            user_data=serializer.data
            print('yes',user_data)
            send_code_to_user(user_data['email'])

            return Response({
                'data':user_data,
                'message':'thanks for signing up a passcode has be sent to verify your email'
            }, status=status.HTTP_201_CREATED)
        
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


        if not  serializer.is_valid(raise_exception=True):
              print(serializer.errors,"yes executed")
              return Response({'data':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class VerifyUserEmail(GenericAPIView):
    def post(self, request):
        try:
            passcode = request.data.get('otp')
            user_pass_obj=OneTimePassword.objects.get(otp=passcode)
            user=user_pass_obj.user
            if not user.is_verified:
                user.is_verified=True
                user.save()
                return Response({
                    'message':'account email verified successfully'
                }, status=status.HTTP_200_OK)
            return Response({'message':'passcode is invalid user is already verified'}, status=status.HTTP_204_NO_CONTENT)
        except OneTimePassword.DoesNotExist as identifier:
            return Response({'message':'passcode not provided'}, status=status.HTTP_400_BAD_REQUEST)


class LoginUserView(GenericAPIView):
    serializer_class=LoginSerializer
    def post(self, request):
        serializer= self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            print('data',serializer.data)
            return Response(serializer.data, status=status.HTTP_200_OK)



class PasswordResetRequestView(GenericAPIView):
    serializer_class=PasswordResetRequestSerializer

    def post(self, request):
        serializer=self.serializer_class(data=request.data, context={'request':request})
        serializer.is_valid(raise_exception=True)
        return Response({'message':'we have sent you a link to reset your password'}, status=status.HTTP_200_OK)
        # return Response({'message':'user with that email does not exist'}, status=status.HTTP_400_BAD_REQUEST)




class PasswordResetConfirm(GenericAPIView):

    def get(self, request, uidb64, token):
        try:
            user_id=smart_str(urlsafe_base64_decode(uidb64))
            user=User.objects.get(id=user_id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({'message':'token is invalid or has expired'}, status=status.HTTP_401_UNAUTHORIZED)
            return Response({'success':True, 'message':'credentials is valid', 'uidb64':uidb64, 'token':token}, status=status.HTTP_200_OK)

        except DjangoUnicodeDecodeError as identifier:
            return Response({'message':'token is invalid or has expired'}, status=status.HTTP_401_UNAUTHORIZED)

class SetNewPasswordView(GenericAPIView):
    serializer_class=SetNewPasswordSerializer

    def patch(self, request):
        serializer=self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        #serializer.save()
        return Response({'success':True, 'message':"password reset is succesful"}, status=status.HTTP_200_OK)


class LogoutView(GenericAPIView):
    serializer_class=LogoutUserSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        try:
            refresh_token = request.data['refresh_token']
            print(f"Received refresh token: {refresh_token}")

            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(status=status.HTTP_200_OK)

        except Exception as e:
             print(f"Error during logout: {str(e)}")
             return Response(status=status.HTTP_400_BAD_REQUEST)

    # def post(self, request):
    #     try:
    #         refresh_token = request.data['refresh_token']
    #         token = RefreshToken(refresh_token)
    #         print(refresh_token)
    #         token.blacklist()
    #         return Response(status=status.HTTP_200_OK)
    #     except Exception as e:
    #         return Response(status=status.HTTP_400_BAD_REQUEST)

    # def post(self, request):
    #     serializer=self.serializer_class(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return Response(status=status.HTTP_204_NO_CONTENT)



@api_view(['GET','POST'])
def addtwono(request):
    if request.method=='GET':
         num1 = float(request.query_params.get('num1'))
         num2 = float(request.query_params.get('num2'))

         result=float(num1+num2)
        
         return Response({"res":result})



    if request.method=='POST':
        print(request.data)
        num1 = (request.data['num1'])
        num2 = (request.data['num2'])
        result=num1+num2
        return Response(result)
    

from apiuser.userdetails import userBio

def refmodule(request):
    user=request.user
    if user.is_authenticated:
        userdetails_instance=userBio(user,user.id)
        print("fetching age from ",userdetails_instance.age)
    
        
        return HttpResponse(userdetails_instance.age)
    else:
        return HttpResponse("User is not authenticated.")
    
    userdetails=userBio.get_logged_in_user_details(request)
    print(userdetails)
    return HttpResponse(userdetails)
