# Generated by Django 4.2.8 on 2024-02-28 15:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0004_hocphan_sotien_remove_hocphandadangky_hocphan_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="hocphanchodangky",
            name="nganhDaoTao",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to="app.nganhdaotao",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="hocphanchodangky",
            name="trangThai",
            field=models.BooleanField(blank=True, default=1),
            preserve_default=False,
        ),
    ]
