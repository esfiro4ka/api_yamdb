from rest_framework_simplejwt.views import TokenVerifyView
from django.urls import path
from rest_framework.routers import DefaultRouter
from api.views import ReviewViewSet


router = DefaultRouter()
router.register(
    r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='reviews'
)


urlpatterns = [
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
