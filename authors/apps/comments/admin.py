from django.contrib import admin
from .models import Comment


class AuthorAdmin(admin.ModelAdmin):
    pass


admin.site.register(Comment, AuthorAdmin)
