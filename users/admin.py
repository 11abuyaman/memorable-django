from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'is_staff', 'is_active',)
    list_filter = ('is_staff', 'is_active',)
    fieldsets = UserAdmin.fieldsets + (
        ('Personal info', {'fields': ('profile_picture', 'birthdate')}),
        ('Permissions', {'fields': ()}),
    )
    add_fieldsets = UserAdmin.add_fieldsets+(
        (None, {
            'classes': ('wide',),
            'fields': ()}),
    )
    search_fields = ('email',)
    ordering = ('email',)


admin.site.register(CustomUser, CustomUserAdmin)
