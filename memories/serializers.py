from rest_framework import serializers
from users.serializers import UserCommentSerializer
from .models import *


class AddCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['author', 'memory', 'body', 'image', 'gif']


class UpdateCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['body']


class CommentSerializer(serializers.ModelSerializer):
    author = UserCommentSerializer()

    class Meta:
        model = Comment
        fields = ['id', 'created_at', 'author', 'body', 'image', 'gif']


class ImageListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['src', 'memory']


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['src']


class MemoryListSerializerMembers(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'profile_picture']


class MemoryListSerializerAuthor(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField('get_full_name')

    def get_full_name(self, obj):
        return obj.get_full_name()

    class Meta:
        model = CustomUser
        fields = ['id', 'profile_picture', 'full_name', 'username']


class MemoryListSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True)
    members = MemoryListSerializerMembers(many=True)
    author = MemoryListSerializerAuthor()
    # comments = CommentSerializer(many=True, source='first_three_comments')
    number_of_comments = serializers.SerializerMethodField()

    def get_number_of_comments(self, obj):
        return obj.comments.count()

    class Meta:
        model = Memory
        fields = ['id', 'author', 'title', 'body', 'members', 'images', 'number_of_comments']


class MemorySerializer(serializers.ModelSerializer):
    # author = UserSerializer()
    images = ImageSerializer(many=True)

    class Meta:
        model = Memory
        fields = ['id', 'title', 'body', 'members', 'images']


class MemoryCommentsSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True)

    class Meta:
        model = Memory
        fields = ['comments']


class UserMemoriesSerializer(serializers.ModelSerializer):
    memories = MemorySerializer(many=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'profile_picture', 'memories']
