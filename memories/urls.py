from django.urls import path
from .views import *

urlpatterns = [
    path('<int:pk>/', MemoryAPI.as_view()),
    path('list/', MemoriesList.as_view()),
    path('update/<int:pk>/', UpdateMemoryAPI.as_view()),
    path('add/', AddMemoryAPI.as_view(), name='add-memory'),
    path('remove/<int:pk>/', RemoveMemoryAPI.as_view(), name='remove-memory'),

    path('comments/list/<int:pk>/', MemoryCommentsListAPI.as_view()),
    path('comments2/list/<int:memory>/', CommentsListAPI.as_view()),
    path('comments/remove/<int:pk>/', RemoveCommentAPI.as_view()),
    path('comments/add/', AddCommentAPI.as_view()),
    path('comments/update/<int:pk>/', UpdateCommentAPI.as_view()),
]
