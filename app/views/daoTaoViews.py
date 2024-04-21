from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from app.models import *
from app.forms import *
from django.contrib.auth.decorators import login_required
import pandas as pd
from django.contrib.auth import  get_user_model

@login_required
def DaoTaoHome(request):
   soThietLap = HocPhanChoDangKy.objects.filter(trangThai = True).count()
   soXetDuyet = HocPhanDaDangKy.objects.filter(trangThai = False).count()
   return render(request, 'DaoTao/daoTaoHome.html', {'soThietLap': soThietLap, 'soXetDuyet': soXetDuyet})

@login_required
def ListThietLapDangKy(request):
   alertContent = request.GET.get('alertContent')
   listThietLap = HocPhanChoDangKy.objects.all().order_by('-id')
   return render(request, 'DaoTao/HocPhan/listThietLapDangKy.html', {'listThietLap': listThietLap, 'alertContent': alertContent})

@login_required
def XemThietLapDangKy(request, id):
   alertContent = request.GET.get('alertContent')
   xemThietLap = get_object_or_404(HocPhanChoDangKy, id=id).hocPhan.all()
   tongSoTin = sum(hocPhan.soTinChi for hocPhan in xemThietLap)
   tongSoTien = sum(hocPhan.soTien for hocPhan in xemThietLap)
   thietLapDangKy = get_object_or_404(HocPhanChoDangKy, id=id)

   if request.method == 'POST':
        thietLapDangKy.trangThai = request.POST.get('trangThai')
        thietLapDangKy.save()
        alert_content = 'Sửa'
        url = reverse('listThietLapDangKy') + f'?alertContent={alert_content}'
        return redirect(url)

   return render(request, 'DaoTao/HocPhan/xemThietLapDangKy.html', {'xemThietLap': xemThietLap, 'tongSoTien': tongSoTien, 'tongSoTin': tongSoTin, 'alertContent': alertContent,'thietLapDangKy' : thietLapDangKy})


@login_required
def NewThietLapDangKy(request):
    cacHeDaoTao = HeDaoTao.objects.all().order_by('-id')
    cacKhoa = Khoa.objects.all().order_by('-id')
    cacNganhDaoTao = NganhDaoTao.objects.all().order_by('-id')
    cacNamHoc = NamHoc.objects.all().order_by('-id')
    cacHocPhan = HocPhan.objects.all().order_by('-id')
    if request.method == 'POST':
        form = HocPhanChoDangKyForm(request.POST)
        if form.is_valid():
            form.save()
            alert_content = 'Thêm'
            url = reverse('listThietLapDangKy') + f'?alertContent={alert_content}'
            return redirect(url)
    else:
        form = HocPhanChoDangKyForm()
    return render(request, 'DaoTao/HocPhan/newThietLapDangKy.html', {'form': form, 'cacHocPhan': cacHocPhan, 'cacNamHoc': cacNamHoc, 'cacHeDaoTao': cacHeDaoTao, 'cacKhoa': cacKhoa, 'cacNganhDaoTao': cacNganhDaoTao})

@login_required
def SuaThietLapDangKy(request, id):

    thietLapDangKy = get_object_or_404(HocPhanChoDangKy, id=id)
    cacHocPhanDuocChon = thietLapDangKy.hocPhan.all()
    cacNganhDaoTao = NganhDaoTao.objects.all().order_by('-id')
    cacNamHoc = NamHoc.objects.all().order_by('-id')
    cacHocPhan = HocPhan.objects.all().order_by('-id')
    if request.method == 'POST':
        thietLapDangKy.namHoc = get_object_or_404(NamHoc, id=request.POST.get('namHoc'))
        thietLapDangKy.namKhoa = request.POST.get('namKhoa')
        thietLapDangKy.hocKy = request.POST.get('hocKy')
        
        hocPhan_ids = request.POST.getlist('hocPhan')  # Retrieve a list of selected hocPhan IDs
        hocPhan_objects = HocPhan.objects.filter(id__in=hocPhan_ids)  # Retrieve the corresponding HocPhan objects
        thietLapDangKy.hocPhan.set(hocPhan_objects)  # Update the many-to-many relationship
        
        thietLapDangKy.trangThai = request.POST.get('trangThai')
        thietLapDangKy.save()
        alert_content = 'Sửa'
        url = reverse('listThietLapDangKy') + f'?alertContent={alert_content}'
        return redirect(url)
    else:
        form = HocPhanChoDangKyForm()
    return render(request, 'DaoTao/HocPhan/suaThietLapDangKy.html', {'form': form,'cacNamHoc': cacNamHoc,'cacHocPhan': cacHocPhan,'thietLapDangKy': thietLapDangKy,'cacNganhDaoTao': cacNganhDaoTao,'cacHocPhanDuocChon': cacHocPhanDuocChon})

@login_required
def XoaThietLapDangKy(request, id):
    thietLapDangKy = get_object_or_404(HocPhanChoDangKy, id=id)
    xemThietLap = thietLapDangKy.hocPhan.all()
    tongSoTin = sum(hocPhan.soTinChi for hocPhan in xemThietLap)
    tongSoTien = sum(hocPhan.soTien for hocPhan in xemThietLap)
    if request.method == 'POST':
        thietLapDangKy.delete()
        alert_content = 'Xóa'
        url = reverse('listThietLapDangKy') + f'?alertContent={alert_content}'
        return redirect(url)

    return render(request, 'DaoTao/HocPhan/xoaThietLapDangKy.html', {'thietLapDangKy': thietLapDangKy,'tongSoTin':tongSoTin,'tongSoTien':tongSoTien})


@login_required
def ListXetDuyetDangKy(request):
   alertContent = request.GET.get('alertContent')
   listXetDuyet = HocPhanDaDangKy.objects.all().filter(trangThai = 0).order_by('-id')
   return render(request, 'DaoTao/XetDuyetDangKy/listXetDuyetDangKy.html', {'listXetDuyet': listXetDuyet, 'alertContent': alertContent})

@login_required
def XetDuyetDangKy(request, id):
    hocPhanDaDangKy = get_object_or_404(HocPhanDaDangKy, id=id)
    cacHocPhanDuocChon = hocPhanDaDangKy.hocPhan.all()
    cacHocPhan = hocPhanDaDangKy.hocPhanChoDangKy.hocPhan.all()
    if request.method == 'POST':
        hocPhanDaDangKy.trangThai = 1
        hocPhanDaDangKy.save()
        hocPhanDuocXetDuyet = HocPhanDuocXetDuyet(hocPhanDaDangKy=hocPhanDaDangKy)
        hocPhanDuocXetDuyet.save()
        soTien =  sum(hocPhan.soTien for hocPhan in hocPhanDaDangKy.hocPhan.all())
        soTinChi =  sum(hocPhan.soTinChi for hocPhan in hocPhanDaDangKy.hocPhan.all())
        thanhToanHocPhi = ThanhToanHocPhi(hocPhanDuocXetDuyet=hocPhanDuocXetDuyet,sinhVien = hocPhanDaDangKy.sinhVien,soTien = soTien, soTinChi=soTinChi, trangThai = 0 , thoiGian = None )
        thanhToanHocPhi.save()
        alert_content = 'Xét duyệt'
        url = reverse('listXetDuyetDangKy') + f'?alertContent={alert_content}'
        return redirect(url)
    else:
        form = HocPhanChoDangKyForm()
    return render(request, 'DaoTao/XetDuyetDangKy/xetDuyetDangKy.html', {'form': form,'cacHocPhan': cacHocPhan,'cacHocPhan': cacHocPhan,'cacHocPhanDuocChon': cacHocPhanDuocChon,'hocPhanDaDangKy': hocPhanDaDangKy,'cacHocPhanDuocChon': cacHocPhanDuocChon})

@login_required
def HuyDangKy(request, id):
    alert_content = 'Hủy'
    hocPhanDaDangKy = get_object_or_404(HocPhanDaDangKy, id=id)
    hocPhanDaDangKy.delete()
    url = reverse('listXetDuyetDangKy') + f'?alertContent={alert_content}'
    return redirect(url)


@login_required
def DropListNganhDaoTao(request):
   listHeDaoTao = HeDaoTao.objects.all().order_by('-id')
   listKhoa = Khoa.objects.all().order_by('-id')
   listNganhDaoTao = NganhDaoTao.objects.all().order_by('-id')
   return render(request, 'DaoTao/ThietLapSinhVien/dropListNganhDaoTao.html', {'listHeDaoTao': listHeDaoTao,'listKhoa': listKhoa,'listNganhDaoTao': listNganhDaoTao})

@login_required
def ListLopHoc(request, id):
    alertContent = request.GET.get('alertContent')
    nganhDaoTao = get_object_or_404(NganhDaoTao, id=id)
    listLopHoc = Lop.objects.filter(nganhDaoTao = id).order_by('-id')
    return render(request, 'DaoTao/ThietLapSinhVien/ThietLapLop/listLopHoc.html', {'listLopHoc': listLopHoc,'nganhDaoTao':nganhDaoTao,'alertContent':alertContent})

@login_required
def NewLop(request,id):
    nganhDaoTao = get_object_or_404(NganhDaoTao, id=id)
    if request.method == 'POST':
        form = LopForm(request.POST)
        if form.is_valid():
            form.save()
            alert_content = 'Thêm'
            url = reverse('listLopHoc', args=[id]) + f'?alertContent={alert_content}'
            return redirect(url)
    else:
        form = LopForm()
    return render(request, 'DaoTao/ThietLapSinhVien/ThietLapLop/newLop.html', {'form': form, 'nganhDaoTao': nganhDaoTao})

@login_required
def XoaLop(request, id):
    lop = get_object_or_404(Lop, id=id)
    idNganhDaoTao = lop.nganhDaoTao.id
    if request.method == 'POST':
        lop.delete()
        alert_content = 'Xóa'
        url = reverse('listLopHoc', args=[idNganhDaoTao]) + f'?alertContent={alert_content}'
        return redirect(url)

    return render(request, 'DaoTao/ThietLapSinhVien/ThietLapLop/xoaLop.html', {'lop': lop})

@login_required
def ListSinhVienLop(request, id):
   alertContent = request.GET.get('alertContent')
   lop = get_object_or_404(Lop, id=id)
   listSinhVien = SinhVien.objects.filter(lop = id).order_by('-id')
   return render(request, 'DaoTao/ThietLapSinhVien/listSinhVienLop.html', {'listSinhVien': listSinhVien,'lop':lop,'alertContent':alertContent})

@login_required
def XemSinhVien(request, id):
   sinhVien = get_object_or_404(SinhVien, id=id)
   listSinhVien = SinhVien.objects.filter(lop = id).order_by('-id')
   return render(request, 'DaoTao/ThietLapSinhVien/xemSinhVien.html', {'sinhVien': sinhVien,'listSinhVien':listSinhVien})

@login_required
def NewSinhVien(request,id):
    lop = get_object_or_404(Lop, id=id)
    if request.method == 'POST':
        form = SinhVienForm(request.POST)
        if form.is_valid():
            form.save()
            alert_content = 'Thêm'
            url = reverse('listSinhVienLop', args=[id]) + f'?alertContent={alert_content}'
            return redirect(url)
    else:
        form = SinhVienForm()
    return render(request, 'DaoTao/ThietLapSinhVien/newSinhVien.html', {'form': form, 'lop': lop})

@login_required
def SuaSinhVien(request, id):
    sinhVien = get_object_or_404(SinhVien, id=id)
    idLop = sinhVien.lop.id
    listLop = Lop.objects.all().order_by('-id')
    if request.method == 'POST':
        sinhVien.lop = get_object_or_404(Lop, id=request.POST.get('lop'))
        sinhVien.gioiTinh = request.POST.get('gioiTinh')
        sinhVien.queQuan = request.POST.get('queQuan')
        sinhVien.ngaySinh = request.POST.get('ngaySinh')
        sinhVien.trangThai = request.POST.get('trangThai')
        sinhVien.save()
        alert_content = 'Sửa'
        url = reverse('listSinhVienLop',args=[idLop]) + f'?alertContent={alert_content}'
        return redirect(url)
    else:
        form = SinhVienForm()
    return render(request, 'DaoTao/ThietLapSinhVien/suaSinhVien.html', {'form': form,'listLop': listLop,'sinhVien':sinhVien})


@login_required
def XoaSinhVien(request, id):
    sinhVien = get_object_or_404(SinhVien, id=id)
    idLop = sinhVien.lop.id
    if request.method == 'POST':
        sinhVien.delete()
        user = get_object_or_404(CustomUser, username = sinhVien.maSV)
        user.delete()
        alert_content = 'Xóa'
        url = reverse('listSinhVienLop', args=[idLop]) + f'?alertContent={alert_content}'
        return redirect(url)
    return render(request, 'DaoTao/ThietLapSinhVien/xoaSinhVien.html', {'sinhVien': sinhVien})

def ExcelImportSinhVien(request,id):
    excel_file = request.FILES['excel_file']
    df = pd.read_excel(excel_file)
    lop = get_object_or_404(Lop, id=id)
    for index, row in df.iterrows():
        obj = SinhVien() 
        maSV = row['Mã sinh viên']
        obj.maSV = maSV
        obj.hoTen = row['Họ tên']
        obj.gioiTinh = row['Giới tính']
        obj.queQuan = row['Quê quán']
        obj.ngaySinh = row['Ngày sinh']
        obj.namKhoa = lop.namKhoa
        obj.lop = lop
        obj.trangThai = 1
        obj.save()
        CustomUser = get_user_model()
        user = CustomUser.objects.create_user(username=maSV, password=maSV,maSinhVien=maSV,role="SinhVien")
        user.save()
    alert_content = 'Thêm'
    url = reverse('listSinhVienLop',args=[id]) + f'?alertContent={alert_content}'
    return redirect(url)

def ExcelImportHocPhan(request):
    excel_file = request.FILES['excel_file']
    df = pd.read_excel(excel_file)
    for index, row in df.iterrows():
        obj = HocPhan() 
        obj.heDaoTao = get_object_or_404(HeDaoTao, tenHeDaoTao = row['Hệ đào tạo'])
        nganhDaoTao = row['Ngành đào tạo']
        nganhDaoTao = nganhDaoTao if pd.notna(nganhDaoTao) else None
        print(nganhDaoTao)
        if nganhDaoTao is not None:
            obj.nganhDaoTao = get_object_or_404(NganhDaoTao, tenNganhDaoTao= nganhDaoTao)
        else:
            obj.nganhDaoTao = None
        obj.maHocPhan = row['Mã học phần']
        obj.tenHocPhan = row['Tên học phần']
        obj.soTinChi = row['Số tín chỉ']
        obj.soTien = row['Số tiền']
        obj.save()
    alert_content = 'Thêm'
    url = reverse('listHocPhan') + f'?alertContent={alert_content}'
    return redirect(url)
@login_required
def ListHocPhan(request):
   alertContent = request.GET.get('alertContent')
   listHocPhan = HocPhan.objects.all().order_by('-id')
   cacKhoa = Khoa.objects.all().order_by('-id')
   cacNganhDaoTao = NganhDaoTao.objects.all().order_by('-id')
   cacHeDaoTao = HeDaoTao.objects.all().order_by('-id')
   return render(request, 'DaoTao/ThietLapHocPhan/listHocPhan.html', {'listHocPhan': listHocPhan,'alertContent': alertContent, 'cacHeDaoTao': cacHeDaoTao,'cacKhoa': cacKhoa,'cacNganhDaoTao': cacNganhDaoTao})

@login_required
def NewHocPhan(request):
    cacKhoa = Khoa.objects.all().order_by('-id')
    cacNganhDaoTao = NganhDaoTao.objects.all().order_by('-id')
    cacHeDaoTao = HeDaoTao.objects.all().order_by('-id')
    if request.method == 'POST':
        form = HocPhanForm(request.POST)
        data_copy = request.POST.copy()
        data_copy['soTien'] = data_copy['soTien'].replace(",", "") 
        form.data = data_copy
        if form.is_valid():
            form.save()
            alert_content = 'Thêm'
            url = reverse('listHocPhan') + f'?alertContent={alert_content}'
            return redirect(url)
    else:
        form = HocPhanForm()
    return render(request, 'DaoTao/ThietLapHocPhan/newHocPhan.html', {'form': form, 'cacHeDaoTao': cacHeDaoTao,'cacKhoa': cacKhoa,'cacNganhDaoTao': cacNganhDaoTao})

@login_required
def SuaHocPhan(request, id):
    hocPhan = get_object_or_404(HocPhan, id=id)
    soTien = format(hocPhan.soTien, ",.0f")

    if request.method == 'POST':
        hocPhan.soTien = request.POST.get('soTien').replace(",", "")
        hocPhan.tenHocPhan = request.POST.get('tenHocPhan')
        hocPhan.soTinChi = request.POST.get('soTinChi')
        hocPhan.save()
        alert_content = 'Sửa'
        url = reverse('listHocPhan') + f'?alertContent={alert_content}'
        return redirect(url)
    else:
        hocPhan = HocPhan.objects.get(id=id)
        form = HocPhanForm()
    return render(request, 'DaoTao/ThietLapHocPhan/suaHocPhan.html', {'form': form,'hocPhan': hocPhan,'soTien':soTien})

@login_required
def XoaHocPhan(request, id):
    hocPhan = get_object_or_404(HocPhan, id=id)
    soTien = format(hocPhan.soTien, ",.0f")
    if request.method == 'POST':
        hocPhan.delete()
        alert_content = 'Xóa'
        url = reverse('listHocPhan') + f'?alertContent={alert_content}'
        return redirect(url)

    return render(request, 'DaoTao/ThietLapHocPhan/xoaHocPhan.html', {'hocPhan': hocPhan, 'soTien': soTien})