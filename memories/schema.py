import graphene
from graphene_django.types import DjangoObjectType, ObjectType
from .models import *
from users.models import CustomUser


class CommentType(DjangoObjectType):
    interfaces = (graphene.Node,)

    class Meta:
        model = Comment


class ImageType(DjangoObjectType):
    interfaces = (graphene.Node,)

    class Meta:
        model = Image


class MemoryType(DjangoObjectType):
    interfaces = (graphene.Node,)
    comments = CommentType()
    images = ImageType()

    class Meta:
        model = Memory


class UserType(DjangoObjectType):
    interfaces = (graphene.Node,)

    class Meta:
        model = CustomUser


class Query(ObjectType):
    memory = graphene.Field(MemoryType, id=graphene.Int())
    memories = graphene.List(MemoryType)
    user = graphene.Field(UserType, id=graphene.Int())
    users = graphene.List(UserType)

    def resolve_memory(self, info, **kwargs):
        memory_id = kwargs.get('id')
        if memory_id is not None:
            return Memory.objects.get(pk=memory_id)
        return None

    def resolve_user(self, info, **kwargs):
        user_id = kwargs.get('id')
        if user_id is not None:
            return CustomUser.objects.get(pk=user_id)
        return None

    def resolve_users(self, info, **kwargs):
        return CustomUser.objects.all()

    def resolve_memories(self, info, **kwargs):
        return Memory.objects.all()

#
# class UserInput(graphene.InputObjectType):
#     id = graphene.ID()
#     firstName = graphene.String()
#
#
# class MemoryInput(graphene.InputObjectType):
#     id = graphene.ID()
#     title = graphene.String()
#     members = graphene.List(UserInput)
#     body = graphene.String()
