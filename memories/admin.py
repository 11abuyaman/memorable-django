from django.contrib import admin
from .models import *


class ImageInline(admin.TabularInline):
    model = Image
    max_num = 10
    extra = 0


class CommentsInline(admin.TabularInline):
    model = Comment
    extra = 0


class MemoryAdmin(admin.ModelAdmin):
    inlines = [
        ImageInline,
        CommentsInline
    ]


admin.site.register(Image)
admin.site.register(Comment)
admin.site.register(Memory, MemoryAdmin)
