from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone
from users.models import User


class Category(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=200
    )
    slug = models.SlugField(
        verbose_name='Слаг',
        unique=True,
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=200
    )
    slug = models.SlugField(
        verbose_name='Слаг',
        unique=True,
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=200,
        db_index=True,
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='Описание',
    )
    year = models.IntegerField(
        validators=[MaxValueValidator(timezone.now().year)],
        verbose_name='Год выпуска',
        db_index=True,
    )
    category = models.ForeignKey(
        Category,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='category',
        verbose_name='Категория',
    )
    genre = models.ManyToManyField(
        Genre,
        through='GenreTitle',
        related_name='genre',
        verbose_name='Жанр',
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title} {self.genre}'


class Review(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews')
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField()
    score = models.IntegerField(
        default=0,
        validators=[MinValueValidator(1),
                    MaxValueValidator(10)],
        db_index=True,
    )
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        unique_together = ('author', 'title')

    def __str__(self) -> str:
        return self.text[:settings.TEXT_LENGTH]


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self) -> str:
        return self.text[:settings.TEXT_LENGTH]
