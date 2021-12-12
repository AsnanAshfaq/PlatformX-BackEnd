from django.urls import include, path
from .views import get_user, get_student_profile, get_student_posts, get_all_users, edit_student, create_student, \
    create_organization, signin, signout, activate_user, password_reset, confirm_password_reset, bot_linked_in, \
    user_query
from .scraper import scrape_articles

urlpatterns = [
    path('', get_user),
    path('student/signup/', create_student),
    path('student/<uuid:id>/', get_student_profile),
    path('student/<uuid:id>/posts/', get_student_posts),
    path('student/edit/', edit_student),
    path('organization/signup/', create_organization),
    path('signin/', signin),
    path('signout/', signout),
    path('password_reset/done/', confirm_password_reset),
    path('password_reset/', password_reset),
    path('all/', get_all_users),
    path('activate/', activate_user),
    path('query/', user_query),
    path('bot/linkedIn/', bot_linked_in),
    path('articles/', scrape_articles),
    path('', include('user.follower.urls')),
    path('profile_image/', include('user.profile_image.urls')),
    path('background_image/', include('user.background_image.urls'))
]
