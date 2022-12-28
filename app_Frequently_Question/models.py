from django.db import models


class Frequently_Question(models.Model):
    class Meta:
        verbose_name = "سوال متداول"
        verbose_name_plural = "سوالات متداول"
        ordering = ['-id']

    question = models.CharField(
        max_length=100,
        null=False,
        blank=False,
        verbose_name='سوال'
    )
    answer = models.TextField(
        null=False,
        blank=False,
        verbose_name="پاسخ"
    )
    show_in_index = models.BooleanField(
        default=False,
        verbose_name="نمایش در صفحه اصلی سایت"
    )

    def __str__(self) -> str:
        return f"{self.question}"
