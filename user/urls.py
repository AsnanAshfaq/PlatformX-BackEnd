from django.urls import include, path
from .views import get_user, get_all_users, create_student, create_organization, signin, activate_user, password_reset, \
    confirm_password_reset

urlpatterns = [
    path('', get_user),
    path('student/signup/', create_student),
    path('organization/signup/', create_organization),
    path('signin/', signin),
    path('password_reset/done/', confirm_password_reset),
    path('password_reset/', password_reset),
    path('all/', get_all_users),
    path('activate/', activate_user),
    path('', include('user.follower.urls')),
    path('profile_image/', include('user.profile_image.urls')),
    path('background_image/', include('user.background_image.urls'))
]
