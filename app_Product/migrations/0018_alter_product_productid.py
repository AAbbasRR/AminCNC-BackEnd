# Generated by Django 4.1.3 on 2022-12-13 14:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_Product', '0017_alter_product_productid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='productId',
            field=models.CharField(default='4f6f558e8544', max_length=12, unique=True, verbose_name='کد رهگیری'),
        ),
    ]
