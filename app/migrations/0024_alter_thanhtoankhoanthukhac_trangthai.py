# Generated by Django 4.2.8 on 2024-03-06 09:29

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0023_alter_blockchain_noidung_alter_kehoachthu_noidung_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="thanhtoankhoanthukhac",
            name="trangThai",
            field=models.BooleanField(blank=True, null=True),
        ),
    ]
