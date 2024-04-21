from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from app.models import *
from app.forms import *
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect


@login_required
def sinhVienHome(request):
    maSinhVien = request.session.get('maSinhVien')
    sinhVien = get_object_or_404(SinhVien, maSV=maSinhVien)
    hoTen = sinhVien.hoTen
    soHocPhi = ThanhToanHocPhi.objects.filter(sinhVien = sinhVien).filter(trangThai = False).count()
    soKhoanThuKhac = ThanhToanKhoanThuKhac.objects.filter(sinhVien = sinhVien).filter(trangThai = False).count()

    return render(request, 'SinhVien/sinhVienHome.html', {'hoTen': hoTen,'soHocPhi':soHocPhi,'soKhoanThuKhac':soKhoanThuKhac})


@login_required
def DangKyTinChi(request):
    alertContent = request.GET.get('alertContent')
    maSinhVien = request.session.get('maSinhVien')
    sinhVien = get_object_or_404(SinhVien, maSV=maSinhVien)
    thietLapDangKy = HocPhanChoDangKy.objects.all().filter(namKhoa=sinhVien.namKhoa, nganhDaoTao=sinhVien.lop.nganhDaoTao, trangThai = 1).order_by('-id').first()
    hocPhanDaDangKy = HocPhanDaDangKy.objects.all().filter(hocPhanChoDangKy=thietLapDangKy, sinhVien = sinhVien).order_by('-id').first()
    hocPhanDuocXetDuyet = HocPhanDuocXetDuyet.objects.filter(hocPhanDaDangKy = hocPhanDaDangKy).first()
    if hocPhanDuocXetDuyet is None and thietLapDangKy is not None:
        if hocPhanDaDangKy is not None:
            cacHocPhanDuocChon = hocPhanDaDangKy.hocPhan.all()
        else:
            cacHocPhanDuocChon = None


        if thietLapDangKy is not None:
            cacHocPhan = thietLapDangKy.hocPhan.all()
        else:
            thietLapDangKy = None
            cacHocPhan = None
    else:
        return render(request, 'SinhVien/DangKyTinChi/dangKyTinChi.html', {'trangThai': False})


    if request.method == 'POST':
        hocPhan_ids = request.POST.getlist('hocPhan')  # Retrieve a list of selected hocPhan IDs
        hocPhans = HocPhan.objects.filter(id__in=hocPhan_ids)  # Retrieve the corresponding HocPhan objects
        
        if hocPhanDaDangKy is not None:
            hocPhanDaDangKy.hocPhan.set(hocPhans)
            hocPhanDaDangKy.save()
        else:
            hocPhanDaDangKy = HocPhanDaDangKy(hocPhanChoDangKy=thietLapDangKy, sinhVien=sinhVien, namHoc=thietLapDangKy.namHoc, namKhoa = thietLapDangKy.namKhoa, hocKy= thietLapDangKy.hocKy,trangThai = 0)
            hocPhanDaDangKy.save()
            hocPhanDaDangKy.hocPhan.set(hocPhans)
            hocPhanDaDangKy.save()

        
        alert_content = 'Đăng ký'
        url = reverse('dangKyTinChi') + f'?alertContent={alert_content}'
        return redirect(url)
    else:
        form = HocPhanChoDangKyForm()
    return render(request, 'SinhVien/DangKyTinChi/dangKyTinChi.html', {'form': form,'thietLapDangKy': thietLapDangKy,'cacHocPhan': cacHocPhan,'cacHocPhanDuocChon': cacHocPhanDuocChon,'alertContent':alertContent})


@login_required
def ListHocPhanDaDangKy(request):
    maSinhVien = request.session.get('maSinhVien')
    sinhVien = get_object_or_404(SinhVien, maSV=maSinhVien)
    cacHocPhanDuyet = HocPhanDuocXetDuyet.objects.all().filter(hocPhanDaDangKy__sinhVien=sinhVien).order_by('-id')
    cacHocPhan = []
    for hocPhan in cacHocPhanDuyet:
        cacHocPhan.append(hocPhan.hocPhanDaDangKy)
    return render(request, 'SinhVien/HocPhanDaDangKy/listHocPhanDaDangKy.html', {'cacHocPhan': cacHocPhan})

class KhoanThanhToan:
    def __init__(self,id, namHoc, hocKy, soTinChi, soTien, trangThai):
        self.id = id
        self.namHoc = namHoc
        self.hocKy = hocKy
        self.soTinChi = soTinChi
        self.soTien = soTien
        self.trangThai = trangThai

@login_required
def ListKhoanThanhToan(request):
    maSinhVien = request.session.get('maSinhVien')
    sinhVien = get_object_or_404(SinhVien, maSV=maSinhVien)
    cacKhoanThanhToan = ThanhToanHocPhi.objects.all().filter(sinhVien=sinhVien)
    listKhoanThanhToan = []
    for khoan in cacKhoanThanhToan:
        listHocPhan = khoan.hocPhanDuocXetDuyet.hocPhanDaDangKy.hocPhan.all()
        id = khoan.id
        namHoc = khoan.hocPhanDuocXetDuyet.hocPhanDaDangKy.namHoc.namHoc
        hocKy = khoan.hocPhanDuocXetDuyet.hocPhanDaDangKy.hocKy
        soTinChi =  sum(hocPhan.soTinChi for hocPhan in listHocPhan)
        soTien =  sum(hocPhan.soTien for hocPhan in listHocPhan)
        trangThai = khoan.trangThai
        khoanThanhToan = KhoanThanhToan(id,namHoc,hocKy,soTinChi,soTien,trangThai)
        listKhoanThanhToan.append(khoanThanhToan)
    listThanhToanKhac = ThanhToanKhoanThuKhac.objects.all().filter(sinhVien=sinhVien).order_by('-id')
    return render(request, 'SinhVien/ThanhToanHocPhi/listKhoanThanhToan.html', {'listKhoanThanhToan': listKhoanThanhToan,'listThanhToanKhac': listThanhToanKhac})

@login_required
def XemThanhToanHocPhi(request,id):
    thanhToanHocPhi = get_object_or_404(ThanhToanHocPhi,id = id)
    return render(request, 'SinhVien/ThanhToanHocPhi/xemThanhToanHocPhi.html', {'thanhToanHocPhi': thanhToanHocPhi})



@login_required
def XemThanhToanKhac(request,id):
    thanhToanKhac = get_object_or_404(ThanhToanKhoanThuKhac,id = id)
    return render(request, 'SinhVien/ThanhToanHocPhi/xemThanhToanKhac.html', {'thanhToanKhac': thanhToanKhac})
