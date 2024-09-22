
from accounts.serializers import *
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import random
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import generics, status, views, permissions
from rest_framework.response import Response
from accounts.helper import send_mail,send_otp_via_email,forget_password_send_email
from .serializers import EmailVerificationSerializer

# from seller.models import seller
# from seller.serializer.seller_config import SellerSerializer




import uuid
# function for create user id
def generate_seller_code(user_id):
    fixed_part = 'abcd'
    return f"{fixed_part}{user_id}"


class CreateUserApi(APIView):
    """ > create new user """
    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            latest_data_new=User.objects.latest('id')
            # send_otp_via_email(serializer.data['email'])
            return Response({'message': 'User created successfully', 'data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response({'message': 'User creation failed', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    


# otp verify 
class VerifyOTP(APIView):
    serializer_class = VerifyAccountSerializer
    def post(self, request):
          try:
              data = request.data
              serializer = VerifyAccountSerializer(data=data)
              if serializer.is_valid():
                  email = serializer.validated_data['email']
                  otp = serializer.validated_data['otp']
                  user = User.objects.filter(email=email).first()
                  if not user:
                      return Response({'status': 400, 'message': 'Invalid email', 'data': {}})
                  if user.otp != otp:
                      return Response({'status': 400, 'message': 'Invalid OTP', 'data': {}})
                  user.is_verified = True
                  user.save()
                  return Response({'status': 200, 'message': 'Account verified', 'data': {}})
              return Response({'status': 400, 'message': 'Something went wrong', 'data': serializer.errors})
          except Exception as e:
              print(e) 


class EmailVerification(APIView):
    serializer_class = LoginSerializer
    def post(self, request):
        serializer = EmailVerificationSerializer(data=request.data)
        # Validate the input data
        if serializer.is_valid():
            email = serializer.validated_data['email']
            # Check if the email exists in the User model
            try:
                user = User.objects.get(email=email)
                return Response(
                    {
                        "message": "Email verified successfully.",
                        "email": user.email
                    },
                    status=status.HTTP_200_OK
                )
            except User.DoesNotExist:
                return Response(
                    {"message": "Email does not exist."},
                    status=status.HTTP_404_NOT_FOUND
                )
        
        # Return errors if validation fails
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
   
   
class LoginAPIView(APIView):
    """ > Login user """
    serializer_class = LoginSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get('email', '')
        password = serializer.validated_data.get('password', '')
        user = authenticate(email=email, password=password)
        if not user:
            raise AuthenticationFailed('Invalid credentials, try again')
        if not user.is_active:
            raise AuthenticationFailed('Account disabled, contact admin')
        # Generate tokens
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)
        return Response({
            'message': 'Login successful',
            'contact_number': user.contact_number,
            'access_token': access_token,
            'refresh_token': refresh_token
        }, status=status.HTTP_200_OK)
    
#  send otp for password reset
class RequestPasswordResetEmail(generics.GenericAPIView):
    serializer_class = ForgetPasswordSerializer  
    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        email = request.data.get('email', '')
        print("email is >>>>>>>>>",email)
        if User.objects.filter(email=email).exists():
          user = User.objects.get(email=email)     
          forget_password_send_email(user.email)
          response = {"success": True, "messsage": "sucefully"}
          return Response(response)
        return Response({'status':400, 'message':'something went wrong', 'data':serializer.errors,})          


# otp varification for password reset
class Reset_Password_VerifyOTP(APIView):
  serializer_class = forgetpassword_Verify_AccountSerializer
  def post(self,request):
    try:
      data=request.data
      serializer=forgetpassword_Verify_AccountSerializer(data=data)
      if serializer.is_valid():
        email=serializer.data['email']
        password_resetotp=serializer.data['password_resetotp']
        password=serializer.data['password']
        user=User.objects.filter(email=email)
        if not user.exists():
          return Response({'status':400,'message':'something went wrong','data':'invaild email',})        
        if user[0].password_resetotp != password_resetotp :
           return Response({'status':400, 'message':'something went wrong', 'data':'invaild otp',})        
        user=user.first()
        user.password = password
        user.save()
        return Response({'status':200,'message':'otp varified','data':{},})         
      return Response({'status':400, 'message':'something went wrong', 'data':serializer.errors,})
    except Exception as e:
      print(e)   



