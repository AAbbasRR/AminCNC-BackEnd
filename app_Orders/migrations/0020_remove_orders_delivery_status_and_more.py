# Generated by Django 4.1.3 on 2022-12-25 10:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_Orders', '0019_alter_orders_tracking_code'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orders',
            name='delivery_status',
        ),
        migrations.AddField(
            model_name='orders',
            name='admin_description',
            field=models.TextField(null=True, verbose_name='توضیحات ادمین'),
        ),
        migrations.AddField(
            model_name='orders',
            name='status',
            field=models.CharField(choices=[('CNS', 'لغو شده'), ('SUC', 'تحویل داده شده'), ('AWC', 'در انتظار تایید'), ('PRE', 'در حال آماده سازی')], default='ANS', max_length=3, verbose_name='وضعیت'),
        ),
        migrations.AlterField(
            model_name='orders',
            name='tracking_code',
            field=models.CharField(default='2cb74116a87a', max_length=12, unique=True, verbose_name='کد رهگیری'),
        ),
    ]