# Generated by Django 4.2.8 on 2024-04-17 12:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0030_hocphan_hedaotao"),
    ]

    operations = [
        migrations.AlterField(
            model_name="hocphan",
            name="nganhDaoTao",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="app.nganhdaotao",
            ),
        ),
    ]
