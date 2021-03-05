from django.core.exceptions import MultipleObjectsReturned
from django.db import IntegrityError
from django.http import JsonResponse, HttpResponse
from rest_framework import generics, views
from rest_framework import permissions
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from .paginations import MemoryCommentsListPagination
from .serializers import *
from django.db.models.signals import post_save
from django.db.models import Q
from itertools import chain
from operator import attrgetter
from .permissions import IsAuthor, IsAuthorOrMember, CommentsListIsAuthorOrMember


class MemoriesList(generics.ListAPIView):
    serializer_class = MemoryListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        owned_memories = Memory.objects.filter(Q(members__id=user.id))
        mentioned_memories = Memory.objects.filter(Q(author__id=user.id))
        memories = sorted(chain(owned_memories, mentioned_memories), key=attrgetter('created_at'), reverse=True)
        return memories


# class UsersAPI(generics.ListAPIView):
#     queryset = CustomUser.objects.all().order_by('-date_joined')
#     serializer_class = UserSerializer
#     # permission_classes = [permissions.IsAuthenticated]


class MemoryAPI(generics.RetrieveAPIView):
    queryset = Memory.objects.all()
    serializer_class = MemorySerializer
    permission_classes = [permissions.IsAuthenticated]


class MemoryCommentsListAPI(generics.RetrieveAPIView):
    queryset = Memory.objects.all()
    serializer_class = MemoryCommentsSerializer
    permission_classes = [IsAuthorOrMember]
    pagination_class = MemoryCommentsListPagination


class CommentsListAPI(generics.ListAPIView):
    serializer_class = CommentSerializer
    permission_classes = [CommentsListIsAuthorOrMember]
    pagination_class = MemoryCommentsListPagination
    lookup_field = 'memory'

    def get_queryset(self):
        comments = Comment.objects.filter(memory__pk=self.kwargs['memory'])
        return comments


class UpdateMemoryAPI(generics.UpdateAPIView):
    queryset = Memory.objects.all()
    serializer_class = MemorySerializer
    # permission_classes = [permissions.IsAuthenticated]


class AddCommentAPI(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = AddCommentSerializer

    def perform_create(self, serializer):
        return serializer.save()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = self.perform_create(serializer)
        instance_serializer = CommentSerializer(instance)
        return Response(instance_serializer.data)


class UpdateCommentAPI(generics.UpdateAPIView):
    queryset = Comment.objects.all()
    serializer_class = UpdateCommentSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthor]


class RemoveCommentAPI(generics.DestroyAPIView):
    queryset = Comment.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsAuthor]


class RemoveMemoryAPI(generics.DestroyAPIView):
    queryset = Memory.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsAuthor]


class AddMemoryAPI(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        print('here we go..')
        try:
            title = request.POST.get('title')
            body = request.POST.get('body')
            feeling = request.POST.get('feeling')
            locked = request.POST.get('locked')
            members = request.POST.get('members')
            images = request.FILES.getlist('images')

            author_object = request.user

            memory = Memory.objects.create(title=title, body=body, author=author_object, feeling=feeling,
                                           locked=bool(locked))
            memory.members.set(members)

            for img in images:
                image = Image.objects.create(src=img, memory=memory)
                print(image)

        except IntegrityError:
            print('IntegrityError')
            return JsonResponse(404, safe=False)

        except MultipleObjectsReturned:
            print('MultipleObjectsReturned')
            return JsonResponse(404, safe=False)

        except Exception as e:
            print(e)
            return JsonResponse(404, safe=False)

        return JsonResponse(200, safe=False)


def add_whatsapp(sender, instance, created, **kwargs):
    if created:
        print(instance.body)


post_save.connect(add_whatsapp, sender=Memory)
