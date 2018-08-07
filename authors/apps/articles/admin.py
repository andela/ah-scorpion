from django.contrib import admin
from .models import Article


class AuthorAdmin(admin.ModelAdmin):
    pass


admin.site.register(Article, AuthorAdmin)
