from django.urls import path
from .views import ListItems, SignUp, Login
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
	path("", ListItems.as_view(), name="list_items"),
	path("sign-up", SignUp.as_view(), name="sign_up"),
	path("login", Login.as_view(), name="login"),
	path("api-token-auth", obtain_auth_token, name="obtain_auth_token")
]