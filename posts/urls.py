from django.urls import include, path
from .views import get_all_posts, create_post, edit_post, create_comment, get_comments, get_user_posts

urlpatterns = [
    path('post/<uuid:id>/comment/', get_comments),
    path('post/comment/create', create_comment),
    path('post/create/', create_post),
    path('post/edit/', edit_post),
    path('post/', get_user_posts),
    path('posts/', get_all_posts),
]
