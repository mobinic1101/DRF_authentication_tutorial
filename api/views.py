from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status as httpstatus
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token

from .models import BlogPost
from .serializers import BlogPostSerializer


# Views
class ListItems(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        items = BlogPost.objects.all()

        serializer = BlogPostSerializer(items, many=True)
        print("type of serializer.data ==> ", type(serializer.data), serializer.data)

        return Response(data=serializer.data, status=httpstatus.HTTP_200_OK)

    def post(self, request):
        data = request.data
        BlogPost.objects.create(**data)
        return Response(status=httpstatus.HTTP_201_CREATED)


class SignUp(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data

        username = data.get("username")
        password = data.get("password")

        if User.objects.filter(username=username).exists():
            return Response(
                data={"error": "user already exist"},
                status=httpstatus.HTTP_400_BAD_REQUEST,
            )

        user = User.objects.create_user(username=username)
        user.set_password(password)
        user.save()
        token, _ = Token.objects.get_or_create(user=user)
        return Response(data={"token": token.key}, status=httpstatus.HTTP_200_OK)


class Login(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data

        username = data.get("username")
        if not User.objects.filter(username=username).exists():
            return Response(
                data={"error": "user doesn't exist"},
                status=httpstatus.HTTP_400_BAD_REQUEST,
            )

        username = data.get("username")
        password = data.get("password")
        print(username, password)
        user = authenticate(username=username, password=password)
        print(user)

        if user is None:
            return Response(
                data={"error": "user is None"},
                status=httpstatus.HTTP_400_BAD_REQUEST,
            )

        token, _ = Token.objects.get_or_create(user=user)
        return Response(data={"token": token}, status=httpstatus.HTTP_200_OK)
