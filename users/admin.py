from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import UserModel, Person, TitlePerson


@admin.register(UserModel)
class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Additional Info', {
            'fields': ('bio', 'birth_date', 'location', 'website', 'profile_picture')
        }),
    )
    list_display = ('username', 'email', 'birth_date', 'location', 'is_staff')
    search_fields = ('username', 'email', 'location')


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('name', 'birth_year', 'death_year')
    search_fields = ('name',)
    list_filter = ('birth_year', 'death_year')


@admin.register(TitlePerson)
class TitlePersonAdmin(admin.ModelAdmin):
    list_display = ('person', 'title', 'role', 'order')
    list_filter = ('role',)
    search_fields = ('person__name', 'title__primary_title')
    autocomplete_fields = ('person', 'title')