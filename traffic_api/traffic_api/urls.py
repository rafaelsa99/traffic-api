"""traffic_api URL Configuration

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
from rest_api import views
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = routers.DefaultRouter()
router.register(r'segment', views.RoadSegmentViewSet) 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('upload/', views.UploadFileView.as_view()),
    path('register/', views.RegisterUserView.as_view()),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('groups/', views.GroupView.as_view()),
    path('', include(router.urls)),
    path('segment/<int:segment>/measurement', views.MeasurementView.as_view()),
    path('segment/<int:segment>/measurement/<int:measurement>/', views.MeasurementDetailView.as_view()),
]
