# Generated by Django 4.2.8 on 2024-02-29 04:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0005_hocphanchodangky_nganhdaotao_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="hocphanchodangky",
            name="namNhapHoc",
            field=models.ForeignKey(
                default=1, on_delete=django.db.models.deletion.CASCADE, to="app.khoahoc"
            ),
            preserve_default=False,
        ),
    ]
