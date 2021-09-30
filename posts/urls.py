from django.urls import include, path, re_path
from .views import get_all_posts, create_post, edit_post, delete_post, get_user_posts, search_post

urlpatterns = [
    path('post/create/', create_post),
    path('post/edit/', edit_post),
    path('post/delete/', delete_post),
    path('post/search/', search_post),
    path('post/', get_user_posts),
    path('posts/', get_all_posts),
    path('post/', include('posts.share.urls')),
    path('post/', include('posts.comment.urls')),
]
