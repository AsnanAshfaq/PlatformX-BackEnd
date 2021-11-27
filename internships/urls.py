from django.urls import include, path, re_path
from .views import get_all_internships, get_organization_internship, get_internship

urlpatterns = [
    path('internship/<uuid:id>/', get_internship),
    path('internship/', get_organization_internship),
    path('internships/', get_all_internships),
]
