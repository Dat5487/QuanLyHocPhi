from app.models import *
from django import forms


class KeHoachThuForm(forms.ModelForm):
    class Meta:
        model = KeHoachThu
        fields = ['khoaHoc', 'dotThu','khoanThu','nganhDaoTao','soTien','ngayBatDau','ngayKetThuc','noiDung']

class ThanhToanKhacForm(forms.ModelForm):
    class Meta:
        model = ThanhToanKhoanThuKhac
        fields = ["sinhVien","khoanThuKhac","hanNop","noiDungThu","soTien"]

class BatchThanhToanKhacForm(forms.ModelForm):
    class Meta:
        model = ThanhToanKhoanThuKhac
        fields = ["khoanThuKhac","hanNop","noiDungThu","soTien"] 

class KhoanThuKhacForm(forms.ModelForm):
    class Meta:
        model = KhoanThuKhac
        fields = ['heDaoTao','khoa','tenKhoan','noiDung','soTien']

class HocPhanForm(forms.ModelForm):
    class Meta:
        model = HocPhan
        fields = ['maHocPhan','tenHocPhan','soTinChi','soTien','heDaoTao','nganhDaoTao']
        widgets = {
            'nganhDaoTao': forms.Select(attrs={'required': False}),
        }

class HocPhanChoDangKyForm(forms.ModelForm):
    class Meta:
        model = HocPhanChoDangKy
        fields = ['hocPhan', 'namHoc','namKhoa', 'hocKy','nganhDaoTao','trangThai']

class LopForm(forms.ModelForm):
    class Meta:
        model = Lop
        fields = ['heDaoTao','nganhDaoTao','khoa','lop','namKhoa']

class SinhVienForm(forms.ModelForm):
    class Meta:
        model = SinhVien
        fields = ['maSV','hoTen','ngaySinh','queQuan','lop','trangThai','namKhoa']

class PaymentForm(forms.Form):
    order_id = forms.CharField(max_length=250)
    order_type = forms.CharField(max_length=20)
    amount = forms.IntegerField()
    order_desc = forms.CharField(max_length=100)
    bank_code = forms.CharField(max_length=20, required=False)
    language = forms.CharField(max_length=2)

class ExcelUploadForm(forms.Form):
    excel_file = forms.FileField()