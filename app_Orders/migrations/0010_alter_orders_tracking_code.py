# Generated by Django 4.1.3 on 2022-12-06 10:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_Orders', '0009_alter_orders_tracking_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='tracking_code',
            field=models.CharField(default='f80721e00aea', max_length=12, unique=True, verbose_name='کد رهگیری'),
        ),
    ]
