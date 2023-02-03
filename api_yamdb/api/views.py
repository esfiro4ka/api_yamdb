from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters
# from django.shortcuts import render
from api.serializers import (ReviewSerializer, TitleSerializer,
                             CategorySerializer, SignUpSerializer,
                             GenreSerializer, CommentSerializer,
                             UserSerializer)
from reviews.models import Title, Category, Genre, Review, User
from api.mixins import CreateListDestroyViewSet
from api.permissions import IsAdminOrReadOnly, IsAdminModeratorAuthorOrReadOnly
from rest_framework import generics
# from reviews.utils import Util
from rest_framework import status
# from rest_framework_simplejwt.tokens import RefreshToken
# from django.contrib.sites.shortcuts import get_current_site
# from django.urls import reverse
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from .tokens import create_jwt_pair_for_user
from django.contrib.auth import authenticate


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
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    filter_backends = (DjangoFilterBackend,)
    permission_classes = (IsAuthenticatedOrReadOnly,)


class UsersViewSet(viewsets.ModelViewSet):
    """Получение списка всех произведений."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # filter_backends = (DjangoFilterBackend,)


# class SignUp(generics.GenericAPIView):
#     serializer_class = SignUpSerializer

#     def post(self, request):
#         data = request.data
#         serializer = self.serializer_class(data=data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         user = serializer.data

#         user_email = User.objects.get(email=user['email'])
#         tokens = RefreshToken.for_user(user_email).access_token

#         current_site = get_current_site(request).domain
#         relative_link = reverse('token_obtain_pair')
#         absurl = (
#             'http://' + current_site + relative_link
#             + '?token=' + str(tokens)
#         )
#         email_body = 'Hi ' + user['username'] + \
#             ' Use the link below to verify your email \n' + absurl
#         data = {'email_body': email_body, 'to_email': user['email'],
#                 'email_subject': 'Verify your email'}

#         Util.send_email(data=data)

#         return response.Response(
#             {'user_data': user, 'access_token': str(tokens)},
#             status=status.HTTP_201_CREATED
#         )

class SignUpView(generics.GenericAPIView):
    serializer_class = SignUpSerializer
    permission_classes = []

    def post(self, request: Request):
        data = request.data

        serializer = self.serializer_class(data=data)

        if serializer.is_valid():
            serializer.save()

            response = {
                "message": "User Created Successfully",
                "data": serializer.data
            }

            return Response(data=response, status=status.HTTP_201_CREATED)

        return Response(
            data=serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class GetTokenFromEmailView(APIView):
    permission_classes = []

    def post(self, request: Request):
        email = request.data.get("email")
        confirmation_code = request.data.get("confirmation_code")

        user = authenticate(email=email, confirmation_code=confirmation_code)

        if user is not None:

            tokens = create_jwt_pair_for_user(user)

            response = {"message": "Login Successfull", "tokens": tokens}
            return Response(data=response, status=status.HTTP_200_OK)

        else:
            return Response(data={"message": "Invalid email or password"})

    def get(self, request: Request):
        content = {"user": str(request.user), "auth": str(request.auth)}

        return Response(data=content, status=status.HTTP_200_OK)


# def profile(request):
#     users = User.objects.all()
#     return render(request, 'templates/profile.html', {'users': users})
