from django.urls import include, path
from .views import get_all_posts, create_post, edit_post, delete_post, get_user_posts

urlpatterns = [
    path('post/create/', create_post),
    path('post/edit/', edit_post),
    path('post/delete/', delete_post),
    path('post/', get_user_posts),
    path('posts/', get_all_posts),
    path('post/share/', include('posts.share.urls')),
    path('post/', include('posts.comment.urls')),
]
