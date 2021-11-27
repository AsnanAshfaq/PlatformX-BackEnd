from django.urls import include, path, re_path

from .views import create_test, get_test, get_all_submission, get_submission, create_submission

urlpatterns = [
    path('test/create/', create_test),
    path('test/<uuid:id>/', get_test),
    path('submissions/<uuid:id>/', get_all_submission),
    path('submission/', create_submission),
    path('submission/<uuid:fypID>/<uuid:submissionID>/', get_submission),

]
