from rest_framework import serializers
from .models import CustomUser


class UserCommentSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField(source='get_full_name')

    def get_full_name(self, obj):
        return obj.first_name + " " + obj.last_name

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'profile_picture', 'full_name']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'profile_picture', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = CustomUser(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UsersListSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField(source='get_full_name')

    def get_full_name(self, obj):
        return obj.first_name + " " + obj.last_name

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'profile_picture', 'full_name']
        

class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['profile_picture']

    # def create(self, validated_data):
    #     password = validated_data.pop('password')
    #     user = CustomUser(**validated_data)
    #     user.set_password(password)
    #     user.save()
    #     return user
