# Generated by Django 4.2.8 on 2024-03-06 10:21

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0024_alter_thanhtoankhoanthukhac_trangthai"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="thanhtoankhoanthukhac",
            name="ghiChu",
        ),
    ]
