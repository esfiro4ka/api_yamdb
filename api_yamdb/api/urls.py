from api.views import (CategoryViewSet, CommentViewSet, CustomTokenObtainView,
                       GenreViewSet, ReviewViewSet, SignUpView, TitleViewSet,
                       UsersViewSet)
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

v1_router = DefaultRouter()
v1_router.register(r'titles', TitleViewSet, basename='titles')
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='reviews'
)
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)
v1_router.register(r'categories', CategoryViewSet, basename='categories')
v1_router.register(r'genres', GenreViewSet, basename='genres')
v1_router.register(r'users', UsersViewSet)


urlpatterns = [
    path('v1/', include(v1_router.urls)),
    path('v1/auth/signup/', SignUpView.as_view(), name='signup'),
    path(
        'v1/auth/token/',
        CustomTokenObtainView.as_view(),
        name='token_obtain_pair'
    ),
    path(
        'v1/auth/token/refresh/',
        TokenRefreshView.as_view(),
        name="token_refresh"
    ),
]
