# Generated by Django 4.1.3 on 2022-12-02 11:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_Orders', '0002_alter_productsmodel_options_alter_orders_total_price_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='tracking_code',
            field=models.CharField(default='88c4396636e8', max_length=12, unique=True, verbose_name='کد رهگیری'),
        ),
    ]
