# Generated by Django 4.2.8 on 2024-03-03 16:23

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0017_alter_payment_vnpay_order_id"),
    ]

    operations = [
        migrations.AddField(
            model_name="thanhtoanhocphi",
            name="soTinChi",
            field=models.IntegerField(default=9),
            preserve_default=False,
        ),
    ]