# Generated by Django 4.1.3 on 2022-12-06 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_Product', '0012_alter_product_productid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='productId',
            field=models.CharField(default='8c43a46e7be3', max_length=12, unique=True, verbose_name='کد رهگیری'),
        ),
    ]