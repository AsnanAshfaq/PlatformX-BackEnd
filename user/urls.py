from django.urls import include, path
from .views import get_user, get_all_users, edit_student, create_student, create_organization, signin, signout, \
    activate_user, password_reset, confirm_password_reset, bot_linked_in

urlpatterns = [
    path('', get_user),
    path('student/signup/', create_student),
    path('student/edit/', edit_student),
    path('organization/signup/', create_organization),
    path('signin/', signin),
    path('signout/', signout),
    path('password_reset/done/', confirm_password_reset),
    path('password_reset/', password_reset),
    path('all/', get_all_users),
    path('activate/', activate_user),
    path('bot/linkedIn/', bot_linked_in),
    path('', include('user.follower.urls')),
    path('profile_image/', include('user.profile_image.urls')),
    path('background_image/', include('user.background_image.urls'))
]
