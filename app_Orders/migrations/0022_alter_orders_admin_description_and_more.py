# Generated by Django 4.1.3 on 2022-12-25 21:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_Orders', '0021_alter_orders_status_alter_orders_tracking_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='admin_description',
            field=models.TextField(blank=True, null=True, verbose_name='توضیحات ادمین'),
        ),
        migrations.AlterField(
            model_name='orders',
            name='tracking_code',
            field=models.CharField(default='4f59df86e5ef', max_length=12, unique=True, verbose_name='کد رهگیری'),
        ),
    ]
