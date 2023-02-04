from rest_framework import serializers
from rest_framework.serializers import ValidationError
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainSerializer
from reviews.models import Review, Title, Category, Genre, User, Comment
from rest_framework_simplejwt.tokens import RefreshToken


class EmailTokenObtainSerializer(TokenObtainSerializer):
    username = serializers.CharField()
    email = serializers.EmailField()


class CustomTokenObtainPairSerializer(TokenObtainSerializer):
    @classmethod
    def get_token(cls, user):
        return RefreshToken.for_user(user)

    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)

        return data


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        validators=[
            UniqueValidator(queryset=User.objects.all())
        ],
        required=True,
    )
    email = serializers.EmailField(
        validators=[
            UniqueValidator(queryset=User.objects.all())
        ],
        required=True,
    )

    class Meta:
        model = User
        fields = '__all__'


class CreateUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        validators=[
            UniqueValidator(queryset=User.objects.all())
        ],
        required=True,
    )
    email = serializers.EmailField(
        validators=[
            UniqueValidator(queryset=User.objects.all())
        ],
        required=True,
    )

    class Meta:
        model = User
        fields = ['username', 'email']

    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data['email'],
            validated_data['username'],
        )
        return user


class UserEditSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("username", "email", "first_name",
                  "last_name", "bio", "role")
        model = User
        read_only_fields = ('role',)


class SignUpSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        validators=[
            UniqueValidator(queryset=User.objects.all())
        ],
        required=True,
    )
    email = serializers.EmailField(
        validators=[
            UniqueValidator(queryset=User.objects.all())
        ],
        required=True,
    )

    class Meta:
        model = User
        fields = ['username', 'email']

    def validate_username(self, value):
        if value.lower() == "me":
            raise serializers.ValidationError("Username 'me' is not valid")
        elif len(value) > 150:
            raise serializers.ValidationError("Invalid field length")
        elif value != r'^[\w.@-]+$':
            raise serializers.ValidationError("Invalid field simbol")
        return value

    def validate_email(self, value):
        lower_email = value.lower()
        if User.objects.filter(email__iexact=lower_email).exists():
            raise serializers.ValidationError("Duplicate")
        return lower_email

    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data['username'],
            validated_data['email']
        )
        return user



class POSTReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        fields = '__all__'
        model = Review
        read_only_fields = ('title',)

    def validate(self, data):
        title_id = self.context['view'].kwargs['title_id']
        author = self.context['request'].user
        if Review.objects.filter(title_id=title_id, author=author).exists():
            raise ValidationError(
                'Нельзя оставлять больше одного отзыва на произведение!'
            )
        return data


class PATCHReviewSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('text', 'score')
        model = Review
        read_only_fields = ('title',)

    def validate(self, data):
        title_id = self.context['view'].kwargs['title_id']
        author = self.context['request'].user
        if not Review.objects.filter(title_id=title_id,
                                     author=author).exists():
            raise ValidationError(
                'Вы не можете редактировать чужой отзыв!'
            )
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        fields = '__all__'
        model = Comment
        read_only_fields = ('review',)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(read_only=True, many=True)
    # rating = serializers.IntegerField()

    class Meta:
        fields = '__all__'
        model = Title
        read_only_fields = ('rating',)
