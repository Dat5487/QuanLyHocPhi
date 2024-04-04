# Generated by Django 4.2.8 on 2024-03-04 11:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0018_thanhtoanhocphi_sotinchi"),
    ]

    operations = [
        migrations.CreateModel(
            name="KhoanThuKhac",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("tenKhoan", models.CharField(max_length=100)),
                ("soTien", models.BigIntegerField()),
                ("noiDung", models.TextField()),
                (
                    "khoa",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="app.khoa",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ThanhToanKhoanThuKhac",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("trangThai", models.BooleanField(blank=True)),
                ("hanNop", models.DateField(blank=True, null=True)),
                ("noiDungThu", models.CharField(blank=True, max_length=100, null=True)),
                ("ghiChu", models.CharField(blank=True, max_length=100, null=True)),
                ("soTien", models.BigIntegerField()),
                ("ngayThem", models.DateTimeField(auto_now_add=True, null=True)),
                (
                    "khoanThuKhac",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="app.khoanthukhac",
                    ),
                ),
                (
                    "sinhVien",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="app.sinhvien"
                    ),
                ),
            ],
        ),
        migrations.RemoveField(
            model_name="khoanthuhocphi",
            name="mucHocPhi",
        ),
        migrations.RemoveField(
            model_name="khoanthuhocphi",
            name="sinhVien",
        ),
        migrations.RemoveField(
            model_name="khoanthunhaphoc",
            name="khoaHoc",
        ),
        migrations.RemoveField(
            model_name="khoanthunhaphoc",
            name="khoanThu",
        ),
        migrations.RemoveField(
            model_name="khoanthunhaphoc",
            name="nganhDaoTao",
        ),
        migrations.DeleteModel(
            name="ChiTraHocPhi",
        ),
        migrations.DeleteModel(
            name="KhoanThuHocPhi",
        ),
        migrations.DeleteModel(
            name="KhoanThuNhapHoc",
        ),
        migrations.DeleteModel(
            name="ThietLapMucHocPhi",
        ),
    ]