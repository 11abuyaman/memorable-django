from rest_framework import permissions
from .models import Memory


class IsAuthorOrMember(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `author` attribute.
    """

    def has_object_permission(self, request, view, obj):
        user = request.user
        members = obj.members.all()
        return obj.author == user or user in members


class CommentsListIsAuthorOrMember(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        # user = request.user
        # members = Memory.objects.filter(pk=obj.memory)
        print(obj)
        return False


class IsAuthor(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `author` attribute.
    """

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user
