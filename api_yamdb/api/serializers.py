from rest_framework import serializers
from rest_framework.serializers import ValidationError

from reviews.models import Review, Title, Category, Genre


class ReviewSerializer(serializers.ModelSerializer):
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
    genre = GenreSerializer(read_only=True, required=False, many=True)

    class Meta:
        fields = '__all__'
        model = Title
