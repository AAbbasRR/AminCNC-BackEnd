# Generated by Django 4.1.3 on 2022-12-13 14:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_Orders', '0013_productsmodel_payable_price_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='tracking_code',
            field=models.CharField(default='4913dd8a785d', max_length=12, unique=True, verbose_name='کد رهگیری'),
        ),
    ]
