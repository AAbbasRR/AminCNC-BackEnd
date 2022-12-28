# Generated by Django 4.1.3 on 2022-12-06 10:54

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Newsletter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='نام')),
                ('email', models.EmailField(max_length=254, verbose_name='ایمیل')),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='تاریخ ایجاد')),
            ],
            options={
                'verbose_name': 'خبرنامه',
                'verbose_name_plural': 'خبرنامه ها',
            },
        ),
    ]
