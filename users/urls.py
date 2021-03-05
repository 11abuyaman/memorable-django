from django.urls import path
from .views import *

urlpatterns = [
    path('', UsersAPI.as_view()),
    path('get/<int:pk>/', UserAPI.as_view()),
    path('update/<int:pk>/', UpdateUserAPI.as_view()),
    path('create/', CreateUserAPI.as_view()),
    path('token-auth/', CustomAuthToken.as_view()),
    path('list/', UsersListAPI.as_view())
]
