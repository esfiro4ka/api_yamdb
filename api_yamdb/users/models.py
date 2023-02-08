from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models


class User(AbstractUser):

    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'

    ROLE_CHOICES = (
        (ADMIN, ADMIN),
        (MODERATOR, MODERATOR),
        (USER, USER)
    )

    username = models.CharField(
        max_length=150,
        unique=True,
        validators=[
            RegexValidator(r'^[\w.@-]+$')
        ]
    )
    email = models.EmailField(
        unique=True,
        max_length=254
    )
    first_name = models.CharField(
        max_length=150,
        blank=True
    )
    last_name = models.CharField(
        max_length=150,
        blank=True
    )
    bio = models.TextField('Биография', blank=True)
    role = models.CharField(
        max_length=max([len(role[0]) for role in ROLE_CHOICES]),
        choices=ROLE_CHOICES,
        default=USER,
    )
    confirmation_code = models.CharField(max_length=150)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        swappable = "AUTH_USER_MODEL"
        ordering = ['username']

    def __str__(self):
        return "{}".format(self.email)

    @property
    def is_admin(self):
        return self.role == self.ADMIN

    @property
    def is_user(self):
        return self.role == self.USER

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR
