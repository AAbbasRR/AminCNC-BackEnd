# Generated by Django 4.1.3 on 2022-11-19 12:59

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('app_Material', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Delivery_mode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mode_name', models.CharField(max_length=25, verbose_name='نام نوع ارسال')),
                ('price', models.CharField(blank=True, default='قیمت متغیر', max_length=25, null=True, verbose_name='قیمت ارسال')),
            ],
            options={
                'verbose_name': 'حالت ارسال',
                'verbose_name_plural': 'حالت ارسال ها',
            },
        ),
        migrations.CreateModel(
            name='Discount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='تعداد تخفیف')),
                ('percent', models.FloatField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='درصد اعمال تخفیف روی قیمت')),
            ],
            options={
                'verbose_name': 'تخفیف',
                'verbose_name_plural': 'تخفیف ها',
            },
        ),
        migrations.CreateModel(
            name='MaterialModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=0, default=0, max_digits=10, verbose_name='قیمت واحد')),
                ('number', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)], verbose_name='تعداد موجود')),
                ('material', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='app_Material.material', verbose_name='نوع ماده')),
            ],
        ),
        migrations.CreateModel(
            name='Picture',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('picture', models.ImageField(upload_to='products/images/')),
            ],
            options={
                'verbose_name': 'عکس',
                'verbose_name_plural': 'عکس ها',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25, verbose_name='نام محصول')),
                ('short_description', models.CharField(max_length=100, verbose_name='توضیحات کوتاه')),
                ('description', models.TextField(blank=True, null=True, verbose_name='توضیحات تکمیلی')),
                ('delivery_modes', models.ManyToManyField(to='app_Product.delivery_mode', verbose_name='انواع ارسال')),
                ('discounts', models.ManyToManyField(to='app_Product.discount', verbose_name='تخفیف ها')),
                ('materials', models.ManyToManyField(through='app_Product.MaterialModel', to='app_Material.material', verbose_name='جنس-سایز-قیمت')),
                ('picture', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_Product.picture', verbose_name='عکس های محصول')),
            ],
            options={
                'verbose_name': 'محصول',
                'verbose_name_plural': 'محصولات',
            },
        ),
        migrations.AddField(
            model_name='materialmodel',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='app_Product.product', verbose_name='محصول'),
        ),
        migrations.AddField(
            model_name='materialmodel',
            name='size',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='app_Material.size', verbose_name='اندازه'),
        ),
    ]