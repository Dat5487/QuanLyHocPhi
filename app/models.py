from django.db import models
from django.contrib.auth.models import AbstractUser

class HeDaoTao(models.Model):
    tenHeDaoTao = models.CharField(max_length=100)

# Khóa nhập học
class KhoaHoc(models.Model):
    namKhoaHoc = models.CharField(max_length=100)

# Năm học
class NamHoc(models.Model):
    namHoc = models.CharField(max_length=100)

class Khoa(models.Model):
    tenKhoa = models.CharField(max_length=100)
    
class NganhDaoTao(models.Model):
    khoa = models.ForeignKey(Khoa, on_delete = models.CASCADE)
    heDaoTao = models.ForeignKey(HeDaoTao, on_delete = models.CASCADE)
    tenNganhDaoTao = models.CharField(max_length=100)

class Lop(models.Model):
    heDaoTao = models.ForeignKey(HeDaoTao, on_delete = models.CASCADE)
    nganhDaoTao = models.ForeignKey(NganhDaoTao, on_delete = models.CASCADE)
    khoaHoc = models.ForeignKey(KhoaHoc, on_delete = models.CASCADE)
    khoa = models.ForeignKey(Khoa, on_delete = models.CASCADE)
    lop = models.CharField(max_length=100)
    namKhoa = models.IntegerField()

    
class SinhVien(models.Model):
    maSV = models.CharField(max_length=10)
    hoTen = models.CharField(max_length=100)
    ngaySinh = models.DateField(blank=True, null=True)
    queQuan = models.CharField(max_length=100)
    lop = models.ForeignKey(Lop, on_delete = models.CASCADE)
    trangThai = models.BooleanField(blank=True)
    namKhoa = models.IntegerField()
    
class KhoanThuKhac(models.Model):
    heDaoTao = models.ForeignKey(HeDaoTao, on_delete = models.CASCADE, blank=True, null=True)
    khoa = models.ForeignKey(Khoa, on_delete = models.CASCADE, blank=True, null=True)
    tenKhoan = models.CharField(max_length=100)
    soTien = models.BigIntegerField()
    noiDung = models.TextField(blank=True, null=True)

class ThanhToanKhoanThuKhac(models.Model):
    khoanThuKhac = models.ForeignKey(KhoanThuKhac, on_delete = models.CASCADE)
    sinhVien = models.ForeignKey(SinhVien, on_delete = models.CASCADE)
    trangThai = models.BooleanField(blank=True, null=True)
    hanNop = models.DateField(blank=True, null=True)
    noiDungThu = models.CharField(max_length=100,blank=True, null=True)
    soTien = models.BigIntegerField()
    ngayThem = models.DateTimeField(auto_now_add=True, blank=True, null=True)

class KeHoachThu(models.Model):
    khoaHoc = models.ForeignKey(KhoaHoc, on_delete = models.CASCADE)
    dotThu = models.IntegerField()
    nganhDaoTao = models.ForeignKey(NganhDaoTao, on_delete = models.CASCADE)
    khoanThu = models.CharField(max_length=100)
    trangThai = models.BooleanField(blank=True, null=True)
    soTien = models.BigIntegerField()
    ngayBatDau = models.DateField(blank=True, null=True)
    ngayKetThuc = models.DateField(blank=True, null=True)
    noiDung = models.TextField(blank=True, null=True)

class CustomUser(AbstractUser):
    # Add any additional fields you need for your user model
    maSinhVien = models.TextField()
    # Example role field
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('user', 'User'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

class Payment_VNPay(models.Model):
    order_id = models.CharField(max_length=200,null=True, blank=True)
    amount = models.FloatField(default=0.0, null=True, blank=True)
    order_desc = models.CharField(max_length=200,null=True, blank=True)
    vnp_TransactionNo = models.CharField(max_length=200,null=True, blank=True)
    vnp_ResponseCode = models.CharField(max_length=200,null=True, blank=True)

class BlockChain(models.Model):
    index = models.IntegerField()
    timestamp = models.TextField()
    maSinhVien = models.TextField()
    maThanhToan = models.TextField()
    soTien = models.BigIntegerField()
    noiDung = models.TextField(blank=True, null=True)
    soGiaoDich = models.BigIntegerField()
    ketQua = models.TextField()
    previous_hash = models.CharField(max_length=256)
    hash = models.CharField(max_length=256)
    nonce = models.IntegerField()

class HocPhan(models.Model):
    maHocPhan = models.TextField()
    tenHocPhan = models.TextField()
    soTinChi = models.IntegerField()
    soTien = models.IntegerField()


class HocPhanChoDangKy(models.Model):
    hocPhan = models.ManyToManyField(HocPhan)
    namHoc = models.ForeignKey(NamHoc, on_delete = models.CASCADE)
    namKhoa = models.IntegerField()
    hocKy = models.BooleanField(blank=True)
    nganhDaoTao = models.ForeignKey(NganhDaoTao, on_delete = models.CASCADE)
    trangThai = models.BooleanField(blank=True)

class HocPhanDaDangKy(models.Model):
    hocPhanChoDangKy = models.ForeignKey(HocPhanChoDangKy, on_delete = models.CASCADE)
    hocPhan = models.ManyToManyField(HocPhan)
    sinhVien = models.ForeignKey(SinhVien, on_delete = models.CASCADE)
    namHoc = models.ForeignKey(NamHoc, on_delete = models.CASCADE)
    namKhoa = models.IntegerField()
    hocKy = models.BooleanField(blank=True)
    trangThai = models.BooleanField(blank=True)

class HocPhanDuocXetDuyet(models.Model):
    hocPhanDaDangKy = models.ForeignKey(HocPhanDaDangKy, on_delete = models.CASCADE)

class ThanhToanHocPhi(models.Model):
    hocPhanDuocXetDuyet = models.ForeignKey(HocPhanDuocXetDuyet, on_delete = models.CASCADE)
    sinhVien = models.ForeignKey(SinhVien, on_delete = models.CASCADE)
    soTien = models.BigIntegerField()
    soTinChi = models.IntegerField()
    trangThai = models.BooleanField(blank=True)
    thoiGian = models.DateTimeField(auto_now_add=True, blank=True, null=True)

