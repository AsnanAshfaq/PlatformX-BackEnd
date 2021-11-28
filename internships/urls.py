from django.urls import include, path, re_path
from .views import get_all_internships, get_organization_internship, get_internship, apply, get_internship_applicants, \
    get_internship_applicant, schedule_meeting

urlpatterns = [

    path('internship/<uuid:id>/apply/', apply),
    path('internship/<uuid:id>/applicant/<uuid:stdid>/meeting/', schedule_meeting),
    path('internship/<uuid:id>/applicant/<uuid:stdid>/', get_internship_applicant),
    path('internship/<uuid:id>/applicants/', get_internship_applicants),
    path('internship/<uuid:id>/', get_internship),
    path('internship/', get_organization_internship),
    path('internships/', get_all_internships),
]
