# Generated by Django 4.1.3 on 2022-12-14 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_Product', '0020_alter_product_productid'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductPreparationTime',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField(verbose_name=' تعداد محصول')),
                ('preparation_time', models.IntegerField(verbose_name='زمان آماده سازی(روز کاری)')),
            ],
            options={
                'verbose_name': 'زمان تحویل محصول',
                'verbose_name_plural': 'زمان تحویل محصولات',
            },
        ),
        migrations.AlterField(
            model_name='product',
            name='productId',
            field=models.CharField(default='e89fd72cf23b', max_length=12, unique=True, verbose_name='کد رهگیری'),
        ),
    ]
