from rest_framework_simplejwt.views import TokenVerifyView
from django.urls import include, path


urlpatterns = [
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
