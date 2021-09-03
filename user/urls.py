from django.urls import include, path
from .views import get_user, get_all_users, create_user, signin, activate_user, password_reset, confirm_password_reset

urlpatterns = [
    path('', get_user),
    path('signup/', create_user),
    path('signin/', signin),
    path('password_reset/done/', confirm_password_reset),
    path('password_reset/', password_reset),
    path('all/', get_all_users),
    path('activate/', activate_user),
    path('', include('user.follower.urls')),
    path('profile_image/', include('user.profile_image.urls'))
]
