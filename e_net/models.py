from django.db import models


class Contact(models.Model):
    email = models.EmailField(verbose_name="Email")
    country = models.CharField(max_length=100, verbose_name="Страна")
    city = models.CharField(max_length=100, verbose_name="Город")
    street = models.CharField(max_length=100, verbose_name="Улица")
    house_number = models.CharField(max_length=10, verbose_name="Номер дома")

    class Meta:
        verbose_name = "Контактная информация"
        verbose_name_plural = "Контактная информация"

    def __str__(self):
        return f"{self.country}, {self.city}, {self.street}, {self.house_number}"


class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    model = models.CharField(max_length=100, verbose_name="Модель")
    release_date = models.DateField(verbose_name="Дата выхода на рынок")

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"

    def __str__(self):
        return f"{self.name} ({self.model})"


class NetworkNode(models.Model):
    class Level(models.IntegerChoices):
        FACTORY = 0, "Завод"
        RETAIL = 1, "Розничная сеть"
        ENTREPRENEUR = 2, "Индивидуальный предприниматель"

    name = models.CharField(max_length=100, verbose_name="Название")
    level = models.IntegerField(
        choices=Level.choices, verbose_name="Уровень в иерархии"
    )
    contact = models.OneToOneField(
        Contact, on_delete=models.CASCADE, verbose_name="Контактная информация"
    )
    products = models.ManyToManyField(Product, verbose_name="Продукты")
    supplier = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Поставщик",
    )
    debt = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        verbose_name="Задолженность перед поставщиком",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Звено сети"
        verbose_name_plural = "Звенья сети"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.get_level_display()}: {self.name}"

    def save(self, *args, **kwargs):
        if not self.pk and self.supplier:
            self.level = self.supplier.level + 1
        super().save(*args, **kwargs)
