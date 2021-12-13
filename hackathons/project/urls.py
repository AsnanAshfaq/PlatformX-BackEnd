from django.urls import path, include
from .views import create_project, edit_project, is_user_project_exists, get_project, get_all_projects, \
    evaluate_project, create_result, get_result

urlpatterns = [
    path('', is_user_project_exists),
    path('all/', get_all_projects),
    path('<uuid:projectID>/', get_project),
    path('<uuid:projectID>/evaluate/', evaluate_project),
    path('create/', create_project),
    path('edit/', edit_project),
    path('result/create/', create_result),
    path('result/', get_result),
]
