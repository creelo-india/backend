from rest_framework import serializers
from accounts.models import User
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.hashers import make_password


from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed
# from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.hashers import make_password
# from rest_framework_simplejwt.tokens import RefreshToken, TokenError



class UserSerializer(serializers.ModelSerializer):
    """ > Register new user serializer """
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)

    class Meta:
        model = User
        fields = ['id', 'contact_number', 'first_name', 'last_name', 'email', 'password']

    def validate_contact_number(self, value):
        if not 10 <= len(str(value)) <= 12:
            raise serializers.ValidationError("Phone number should be between 10 and 12 digits")
        return value

    def validate(self, data):
        contact_number = data.get('contact_number')
        city=data.get('city')
        email = data.get('email')
        if city:
            raise serializers.ValidationError("city shuld be str")
        if User.objects.filter(contact_number=contact_number).exists():
            raise serializers.ValidationError("Mobile number already exists")
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("Email already exists")

        if data.get('password'):
            data['password'] = make_password(data['password'])
        return data

# otp verify serilizer
class VerifyAccountSerializer(serializers.Serializer):
    email=serializers.EmailField()
    otp=serializers.CharField()   


# user login serializer
# from rest_framework import serializers
# from django.contrib.auth import authenticate
# from accounts.models import User  # Assuming User model is in 'accounts' app
# from rest_framework.exceptions import AuthenticationFailed


class EmailVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField()

class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255, min_length=3)
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)


class ForgetPasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email']

class forgetpassword_Verify_AccountSerializer(serializers.Serializer):
    password = serializers.CharField(
        max_length=68, min_length=6)
    email=serializers.EmailField()
    password_resetotp=serializers.CharField()
    
    class Meta:
      model = User
      fields = ['email','password','password_resetotp']
    def validate(self, data):
        if data.get('password'):
            data['password'] = make_password(data['password'])
        return data
