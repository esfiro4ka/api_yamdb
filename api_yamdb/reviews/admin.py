from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from reviews.models import Category, Comment, Genre, Review, Title, User


class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('email', 'username',)


class TitleAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'category',)
    search_fields = ('name',)
    list_filter = ('category',)
    empty_value_display = '-пусто-'


admin.site.register(Title, TitleAdmin)
admin.site.register(Category)
admin.site.register(Genre)
admin.site.register(Review)
admin.site.register(Comment)
admin.site.register(User, CustomUserAdmin)
