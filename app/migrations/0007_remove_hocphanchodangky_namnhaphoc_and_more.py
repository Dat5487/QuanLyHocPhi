# Generated by Django 4.2.8 on 2024-02-29 04:20

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0006_hocphanchodangky_namnhaphoc"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="hocphanchodangky",
            name="namNhapHoc",
        ),
        migrations.AddField(
            model_name="hocphanchodangky",
            name="nienKhoa",
            field=models.TextField(default=-4),
            preserve_default=False,
        ),
    ]
