# Generated by Django 4.1.3 on 2023-01-13 11:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_Product', '0028_alter_product_productid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='productId',
            field=models.CharField(default='8d3ebc964932', max_length=12, unique=True, verbose_name='کد رهگیری'),
        ),
    ]