# Generated by Django 4.1.3 on 2022-12-06 10:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_Product', '0009_alter_product_productid'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='discount',
            options={'ordering': ['number'], 'verbose_name': 'تخفیف', 'verbose_name_plural': 'تخفیف ها'},
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['-created_date'], 'verbose_name': 'محصول', 'verbose_name_plural': 'محصولات'},
        ),
        migrations.AlterField(
            model_name='product',
            name='productId',
            field=models.CharField(default='fbca9a81a453', max_length=12, unique=True, verbose_name='کد رهگیری'),
        ),
    ]
