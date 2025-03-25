from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Модель пользователя."""
    username = None
    email = models.EmailField(unique=True, verbose_name="Электронная почта")

    first_name = models.CharField(
        max_length=50,
        verbose_name="Имя",
        blank=True,
        null=True,
        help_text="Введите имя",
    )

    last_name = models.CharField(
        max_length=50,
        verbose_name="Фамилия",
        blank=True,
        null=True,
        help_text="Введите фамилию",
    )

    patronymic = models.CharField(
        max_length=50,
        verbose_name="Отчество",
        blank=True,
        null=True,
        help_text="Введите отчество (при наличии)",
    )

    phone_number = models.CharField(
        max_length=35,
        verbose_name="Номер телефона",
        blank=True,
        null=True,
        help_text="Введите номер телефона",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь 'E_net'"
        verbose_name_plural = "Пользователи 'E_net'"

    def __str__(self):
        return self.email
