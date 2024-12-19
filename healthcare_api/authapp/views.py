from rest_framework.views import APIView
from .serializers import UserSerializer
from .models import CustomUser
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken  
from django.utils.timezone import now

class RegisterView(APIView):
  def post(sef, request):
    serializer  = UserSerializer(data = request.data)
    if serializer.is_valid():
      user = serializer.save()
      
      # Generate access and refresh tokens
      refresh = RefreshToken.for_user(user)
      access_token = str(refresh.access_token)
            
      response = {
        "meta":{
          "created_at": serializer.data["created_at"],
          "timestamp": str(now()),
        },
        "data": {
          "name": serializer.data["name"],
          "age": serializer.data["age"],
          "email": serializer.data["email"],
          "ph_num": serializer.data["ph_num"],
          "access": access_token,
          "refresh": str(refresh),
        },
      }
      return Response(response, status=status.HTTP_201_CREATED)
    else:
      response = {
          "meta":{
            "timestamp": str(now()),
          },
          "errors": serializer.errors,
          "links": {
            "swagger": "http://127.0.0.1:8000/swagger",
            "redoc": "http://127.0.0.1:8000/redoc",
          }
        }
      return Response(response, status=status.HTTP_400_BAD_REQUEST)
    
class LoginView(APIView):
  def post(self, request):
    email = request.data.get("email")
    password = request.data.get("password")
        
    if not email or not password:
      response = {
          "meta":{
            "timestamp": str(now()),
          },
          "errors":{
            "email": "Email is required.",
            "password": "Password is required."
          },
          "links": {
            "swagger": "http://127.0.0.1:8000/swagger",
            "redoc": "http://127.0.0.1:8000/redoc",
            "login":"http://127.0.0.1:8000/api/login",            
          }
        }
      return Response(response,status=status.HTTP_400_BAD_REQUEST)

    user = CustomUser.objects.filter(email = email).first()
        
    if not user:
      response = {
          "meta":{
            "timestamp": str(now()),
          },
          "errors": "User not found!",
          "links": {
            "swagger": "http://127.0.0.1:8000/swagger",
            "redoc": "http://127.0.0.1:8000/redoc",
            "login":"http://127.0.0.1:8000/api/login",
          }
        }
      return Response(response,status=status.HTTP_404_NOT_FOUND)
    
    if not user.check_password(password):
      response = {
          "meta":{
            "timestamp": str(now()),
          },
          "errors": "Incorrect Password!",
          "links": {
            "swagger": "http://127.0.0.1:8000/swagger",
            "redoc": "http://127.0.0.1:8000/redoc",
            "login":"http://127.0.0.1:8000/api/login",
          }
        }
      return Response(response,status=status.HTTP_401_UNAUTHORIZED)
       
      
    # Generate access and refresh tokens
    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)
    
    response = {
      "meta":{
        "timestamp": str(now()),
      },
      "data":{
        "access": access_token,
        "refresh": str(refresh),
      }
    }
    
    return Response(response, status=status.HTTP_200_OK)