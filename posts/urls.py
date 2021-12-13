from django.urls import include, path, re_path
from .views import get_all_posts, create_post, edit_post, delete_post, get_user_posts, search_post, get_saved_posts, \
    save_post

urlpatterns = [
    path('post/create/', create_post),
    path('post/edit/', edit_post),
    path('post/delete/', delete_post),
    path('post/search/', search_post),
    path('post/', get_user_posts),
    path('post/<uuid:id>/save/', save_post),
    path('posts/saved/', get_saved_posts),
    path('posts/', get_all_posts),
    path('post/', include('posts.share.urls')),
    path('post/', include('posts.comment.urls')),
]
