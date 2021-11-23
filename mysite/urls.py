"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from fcm_django.api.rest_framework import FCMDeviceAuthorizedViewSet
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('posts.urls')),
    path('api/', include('hackathons.urls')),
    path('api/', include('workshop.urls')),
    path('api/', include('fyp.urls')),
    path('api/', include('sphere_engine.urls')),
    path('user/', include('user.urls')),
    path('chat/', include('chat.urls')),
    path('payment/', include('payment.urls')),
    # firebase cloud messaging route
    path('devices/', FCMDeviceAuthorizedViewSet.as_view({'get': 'list'}), name='create_fcm_device'),
    # path('accounts/',include('django.contrib.auth.urls')),
    # path('api-token-auth/', views.obtain_auth_token, name='api-tokn-auth'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# urlpatterns += [
#     path('accounts/', include('django.contrib.auth.urls')),
# ]
