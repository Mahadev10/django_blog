from django.urls import path
from . import views
urlpatterns = [
    path('',views.home,name="home"),
    path('posts/<slug:slug>',views.detailPost,name="post_detail"),
    path('categories/<str:category_name>',views.categoryPosts,name="category_posts"),
    path('tags/<str:tag_name>',views.tagPosts,name="tag_posts"),
    path('like/<slug:slug>',views.likePost,name="like_post"),
    path('search/',views.searchPosts,name="search_posts"),
]