from django.db import models
from django.utils import timezone


class Newsletter(models.Model):
    class Meta:
        verbose_name = 'خبرنامه'
        verbose_name_plural = 'خبرنامه ها'

    name = models.CharField(
        max_length=150,
        verbose_name='نام'
    )
    email = models.EmailField(
        verbose_name='ایمیل'
    )
    created_date = models.DateTimeField(
        default=timezone.now,
        verbose_name='تاریخ ایجاد'
    )

    def __str__(self):
        return f'{self.name} - {self.email}'
