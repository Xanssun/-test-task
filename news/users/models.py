from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    username = models.CharField(
        'Логин',
        max_length=150,
        unique=True,
        null=False
    )
    password = models.CharField(
        'Пароль',
        max_length=150,
        blank=False,
        null=False
    )

    email = models.EmailField(
        'Почта',
        max_length=250,
        unique=True,
        null=False
    )

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        constraints = [
            models.UniqueConstraint(
                fields=['email', 'username'],
                name='unique_username_email'
            )
        ]

    def __str__(self):
        return self.username
