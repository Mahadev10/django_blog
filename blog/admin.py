from django.contrib import admin
from . import models

@admin.register(models.Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'slug', 'short_description', 'content',
                    'status', 'published_at', 'updated_at', 'category', 'author')
    populated_fields = {'slug',('title',)}                

@admin.register(models.Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at', 'updated_at', 'active')

@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at', 'updated_at', 'active')
@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display=('id','comment_text','created_at','updated_at','active')
@admin.register(models.Like)
class LikeAdmin(admin.ModelAdmin):
    list_display=('post','user')