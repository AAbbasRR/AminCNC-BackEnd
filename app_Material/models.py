from django.db import models
from django.core.validators import MinValueValidator


class Material(models.Model):
    class Meta:
        verbose_name = "متریال"
        verbose_name_plural = f"{verbose_name} ها"

    color = models.CharField(
        max_length=25,
        null=False,
        blank=False,
        verbose_name='رنگ'
    )
    ingredient = models.CharField(
        max_length=25,
        null=False,
        blank=False,
        verbose_name='جنس'
    )
    description = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name='توضیحات'
    )

    def __str__(self) -> str:
        return f"{self.ingredient} با رنگ: {self.color}"


class Size(models.Model):
    class Meta:
        verbose_name = "اندازه"
        verbose_name_plural = f"{verbose_name} ها"

    width = models.FloatField(
        validators=[MinValueValidator(0), ],
        null=False,
        blank=False,
        verbose_name='عرض(سانتی متر)'
    )
    length = models.FloatField(
        validators=[MinValueValidator(0), ],
        null=False,
        blank=False,
        verbose_name='طول(سانتی متر)'
    )
    height = models.FloatField(
        validators=[MinValueValidator(0), ],
        null=True,
        blank=True,
        verbose_name='عرض(سانتی متر)'
    )

    def __str__(self) -> str:
        return f"{self.width}*{self.length}{f'*{self.height}' if self.height is not None else ''}"
