from django.urls import path, include
from .views import create_project, edit_project, is_user_project_exists, get_project

urlpatterns = [
    path('', is_user_project_exists),
    path('<uuid:projectID>/', get_project),
    path('create/', create_project),
    path('edit/', edit_project),

]
