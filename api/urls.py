from django.urls import path, include
from rest_framework import routers
from api import views
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from .views import CustomTokenObtainPairView, CustomLoginView,CustomRegisterView

router = routers.DefaultRouter()
router.register(r'armas',views.ArmaViewSet)

urlpatterns = [
    path('',include(router.urls)),
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('login/', CustomLoginView.as_view(), name='custom_rest_login'),
    path('register/', CustomRegisterView.as_view(), name='custom_rest_register'),
    path('authentication/', include('dj_rest_auth.urls')),
]

