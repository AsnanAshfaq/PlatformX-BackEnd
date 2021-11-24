from django.urls import include, path, re_path

from .views import create_test, get_test, get_submission

urlpatterns = [
    path('test/create/', create_test),
    path('test/<uuid:id>/', get_test),
    path('submission/<uuid:id>/', get_submission),
]
