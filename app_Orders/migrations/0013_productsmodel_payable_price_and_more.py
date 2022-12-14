# Generated by Django 4.1.3 on 2022-12-13 10:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_Orders', '0012_productsmodel_discount_price_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='productsmodel',
            name='payable_price',
            field=models.DecimalField(decimal_places=0, default=0, max_digits=10, verbose_name='جمع قیمت قابل پرداخت(تومان)'),
        ),
        migrations.AlterField(
            model_name='orders',
            name='tracking_code',
            field=models.CharField(default='78bc78fe8f6e', max_length=12, unique=True, verbose_name='کد رهگیری'),
        ),
    ]
