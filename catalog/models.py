from django.db import models


class Category(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name="Наименование",
        help_text="Введите наименование категории",
    )
    description = models.TextField(
        verbose_name="Описание",
        help_text="Введите описание категории",
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(
        max_length=100, verbose_name="Наименование", help_text="Наименование товара"
    )
    description = models.CharField(
        max_length=100, verbose_name="Описание", help_text="Описание товара"
    )
    image = models.ImageField(
        upload_to="catalog/images",
        blank=True,
        null=True,
        verbose_name="Изображение",
        help_text="Изображение товара",
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        max_length=100,
        verbose_name="Категория",
        help_text="Категория товара",
        null=True,
        blank=True,
        related_name="products",
    )
    purchase_price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Цена", help_text="Цена товара"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        ordering = ["created_at", "updated_at"]

    def __str__(self):
        return self.name
