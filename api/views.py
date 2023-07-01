from django.contrib.auth import login
from django.contrib.auth.password_validation import validate_password

from email_validator import validate_email, EmailNotValidError

from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.serializers import AuthTokenSerializer

from .serializers import UserSerializer
from .models import User

from knox.auth import TokenAuthentication
from knox.views import LoginView as KnoxLoginView


class UserView(APIView):
    '''
    Return or Updates the data of the user
    '''
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request, format=None):
        userserializer = UserSerializer(request.user)
        return Response(userserializer.data)

    def put(self, request, format=None):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        user = request.user
        if not username and not email and not password:
            return Response({'error': 'no fields provided to update. Please provide username or email or password to update'}, status=status.HTTP_400_BAD_REQUEST)
        if email:
            try:
                emailinfo = validate_email(email, check_deliverability=True)
                email = emailinfo.normalized
                user.email = email
                user.save()
            except EmailNotValidError as e:
                return Response(e, status=status.HTTP_400_BAD_REQUEST)
        if password:
            try:
                validate_password(password)
                user.set_password(password)
                user.save()
            except:
                return Response({'error': 'The password is not strong. Please use at least 8 characters and make sure there is at least one of number, lowercase, uppercase and special characters each'}, status=status.HTTP_400_BAD_REQUEST)
        if username:
            try:
                user.username = username
                user.save()
            except:
                return Response({'error': 'error changing username'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_201_CREATED)


class UserRegisterView(APIView):
    '''
    Registers the user and returns the token as authentication
    '''
    permission_classes = [permissions.AllowAny]

    def post(self, request, format=None):
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')
        if not username or not password or not email:
            return Response({"error": "username or password or email not provided"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            emailinfo = validate_email(email, check_deliverability=True)
            email = emailinfo.normalized
        except EmailNotValidError as e:
            return Response(e, status=status.HTTP_400_BAD_REQUEST)
        try:
            validate_password(password)
        except:
            return Response({'error': 'The password is not strong. Please use at least 8 characters and make sure there is at least one of number, lowercase, uppercase and special characters each'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.create_user(
                username=username, email=email, password=password)
        except:
            return Response({'error': 'Duplicate Username'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'username': user.username}, status=status.HTTP_201_CREATED)


class LoginView(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginView, self).post(request, format=None)
