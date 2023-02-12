from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from authentication import views
from authentication.views import MyTokenObtainPairView

urlpatterns = [
    path('reset_password', views.reset_password),
    path('categories', views.get_categories),
    path('', views.UserViewSet.as_view({'post': 'create', 'get': 'retrieve', 'put': 'update'})),
    path('api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]