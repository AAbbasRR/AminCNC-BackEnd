# Generated by Django 4.1.3 on 2022-12-04 15:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_Product', '0008_product_show_in_index_alter_product_productid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='productId',
            field=models.CharField(default='838b4634587e', max_length=12, unique=True, verbose_name='کد رهگیری'),
        ),
    ]