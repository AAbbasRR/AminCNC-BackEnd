# Generated by Django 4.1.3 on 2023-01-11 21:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('app_Orders', '0024_alter_orders_tracking_code'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=0, default=0, max_digits=10, verbose_name='مبلغ پرداخت شده(تومان)')),
                ('date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='تاریخ ثبت سفارش')),
                ('status', models.CharField(choices=[('CNS', 'لغو شده'), ('SUC', 'پرداخت شده')], default='CNS', max_length=3, verbose_name='وضعیت')),
                ('portal', models.CharField(choices=[('ZPL', 'زرینپال')], default='ZPL', max_length=3, verbose_name='درگاه پرداخت')),
                ('ref_id', models.CharField(max_length=50, verbose_name='کد پیگیری')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='app_Orders.orders', verbose_name='سفارش')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),
            ],
            options={
                'verbose_name': 'تاریخچه تراکنش',
                'verbose_name_plural': 'تاریخچه تراکنش ها',
            },
        ),
    ]