from django.shortcuts import get_object_or_404
from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters
from api.serializers import (ReviewSerializer, TitleSerializer,
                             CategorySerializer, SignUpSerializer,
                             GenreSerializer, CommentSerializer,
                             UserSerializer, TokenSerializer)
from reviews.models import Title, Category, Genre, Review, User
from api.filters import TitlesFilter
from api.mixins import CreateListDestroyViewSet
from api.permissions import (IsAdminOrReadOnly,
                             IsAdminModeratorAuthorOrReadOnly)
from rest_framework import generics
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,
                          IsAdminModeratorAuthorOrReadOnly,)

    def get_title(self):
        return get_object_or_404(Title, id=self.kwargs['title_id'])

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())

    def get_queryset(self):
        title = self.get_title()
        return title.reviews.all()


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,
                          IsAdminModeratorAuthorOrReadOnly,)

    def get_review(self):
        return get_object_or_404(Review, id=self.kwargs['review_id'])

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.get_review())

    def get_queryset(self):
        review = self.get_review()
        return review.comments.all()


class CategoryViewSet(CreateListDestroyViewSet):
    """Получение списка всех категорий."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAuthenticatedOrReadOnly,
                          IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenreViewSet(CreateListDestroyViewSet):
    """Получение списка всех жанров."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,
                          IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    """Получение списка всех произведений."""
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')).order_by('-rating')
    serializer_class = TitleSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitlesFilter
    permission_classes = (IsAuthenticatedOrReadOnly,)


class SignUpView(generics.GenericAPIView):
    """Регистрация пользователя по email"""

    serializer_class = SignUpSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        if User.objects.filter(
            username=request.data.get('username'),
            email=request.data.get('email')
        ).exists():
            return Response(request.data, status=status.HTTP_200_OK)

        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        user = get_object_or_404(
            User,
            username=serializer.validated_data["username"]
        )
        confirmation_code=default_token_generator.make_token(user)


        email_subject="Activate your Account"
        email_body=f'Your confirmation code: {confirmation_code}',

        send_mail(
            email_subject,
            email_body,
            settings.EMAIL_HOST_USER,
            [user_data['email'],]
        )
            
        return Response(serializer.data, status=status.HTTP_200_OK)


def get_token(request):
    serializer = TokenSerializer(data=request.data)
    permission_classes = (AllowAny,)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(
        User,
        username=serializer.validated_data["username"]
    )

    if default_token_generator.check_token(
        user, serializer.validated_data["confirmation_code"]
    ):
        token = AccessToken.for_user(user)
        return Response({"token": str(token)}, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UsersViewSet(viewsets.ModelViewSet):
    """Получение списка всех произведений."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # filter_backends = (DjangoFilterBackend,)
    permission_classes = (IsAdminOrReadOnly,)
