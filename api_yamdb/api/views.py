from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters

from api.serializers import (ReviewSerializer, TitleSerializer,
                             CategorySerializer, SignUpSerializer,
                             GenreSerializer)
from reviews.models import Title, Category, User, Genre
from api.mixins import CreateListDestroyViewSet
from api.permissions import IsAdminOrReadOnly
from rest_framework import generics
from reviews.utils import Util
from rest_framework import response, status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer

    def get_title(self):
        return get_object_or_404(Title, id=self.kwargs['title_id'])

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())

    def get_queryset(self):
        title = self.get_title()
        return title.reviews.all()


class CategoryViewSet(CreateListDestroyViewSet):
    """Получение списка всех категорий."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly, )
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenreViewSet(CreateListDestroyViewSet):
    """Получение списка всех жанров."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly, )
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    """Получение списка всех произведений."""
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    filter_backends = (DjangoFilterBackend,)


class SignUp(generics.GenericAPIView):
    serializer_class = SignUpSerializer

    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user = serializer.data

        user_email = User.objects.get(email=user['email'])
        tokens = RefreshToken.for_user(user_email).access_token

        current_site = get_current_site(request).domain
        relative_link = reverse('token_verify')
        absurl = (
            'http://' + current_site + relative_link + '?token=' + str(tokens)
        )
        email_body = 'Hi ' + user['username'] + \
            ' Use the link below to verify your email \n' + absurl
        data = {'email_body': email_body, 'to_email': user['email'],
                'email_subject': 'Verify your email'}

        Util.send_email(data=data)

        return response.Response(
            {'user_data': user, 'access_token': str(tokens)},
            status=status.HTTP_201_CREATED
        )