from rest_framework.routers import DefaultRouter

from api.views import ReviewViewSet


router = DefaultRouter()
router.register(
    r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='reviews'
)
