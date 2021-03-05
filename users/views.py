from .models import CustomUser
from rest_framework import generics
from rest_framework import permissions
from .serializers import UserSerializer, UpdateUserSerializer, UsersListSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import filters


class CreateUserAPI(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)


class UsersAPI(generics.ListAPIView):
    queryset = CustomUser.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    # permission_classes = [permissions.IsAuthenticated]


class UserAPI(generics.RetrieveAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    # permission_classes = [permissions.IsAuthenticated]


class UpdateUserAPI(generics.UpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UpdateUserSerializer
    # permission_classes = [permissions.IsAuthenticated]


class UsersListAPI(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UsersListSerializer
    # permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['first_name', 'last_name', 'username']


class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        print('user.profile_picture')
        if user.profile_picture:
            return Response({
                'token': token.key,
                'user_id': user.pk,
                'email': user.email,
                'profile_picture': user.profile_picture.url
            })
        else:
            return Response({
                'token': token.key,
                'user_id': user.pk,
                'email': user.email,
            })
