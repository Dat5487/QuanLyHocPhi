from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from app.models import *
from app.forms import *
from django.contrib.auth.decorators import login_required


@login_required
def CanBoHome(request):
   return render(request, 'CanBo/canBoHome.html')

@login_required
def ListThietLapDangKy(request):
   alertContent = request.GET.get('alertContent')
   listThietLap = HocPhanChoDangKy.objects.all().order_by('-id')
   return render(request, 'CanBo/HocPhan/listThietLapDangKy.html', {'listThietLap': listThietLap, 'alertContent': alertContent})

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

   return render(request, 'CanBo/HocPhan/xemThietLapDangKy.html', {'xemThietLap': xemThietLap, 'tongSoTien': tongSoTien, 'tongSoTin': tongSoTin, 'alertContent': alertContent,'thietLapDangKy' : thietLapDangKy})


@login_required
def NewThietLapDangKy(request):
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
    return render(request, 'CanBo/HocPhan/newThietLapDangKy.html', {'form': form, 'cacHocPhan': cacHocPhan, 'cacNamHoc': cacNamHoc, 'cacNganhDaoTao': cacNganhDaoTao})

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
    return render(request, 'CanBo/HocPhan/suaThietLapDangKy.html', {'form': form,'cacNamHoc': cacNamHoc,'cacHocPhan': cacHocPhan,'thietLapDangKy': thietLapDangKy,'cacNganhDaoTao': cacNganhDaoTao,'cacHocPhanDuocChon': cacHocPhanDuocChon})

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

    return render(request, 'CanBo/HocPhan/xoaThietLapDangKy.html', {'thietLapDangKy': thietLapDangKy,'tongSoTin':tongSoTin,'tongSoTien':tongSoTien})


@login_required
def ListXetDuyetDangKy(request):
   alertContent = request.GET.get('alertContent')
   listXetDuyet = HocPhanDaDangKy.objects.all().filter(trangThai = 0).order_by('-id')
   return render(request, 'CanBo/XetDuyetDangKy/listXetDuyetDangKy.html', {'listXetDuyet': listXetDuyet, 'alertContent': alertContent})

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
    return render(request, 'CanBo/XetDuyetDangKy/xetDuyetDangKy.html', {'form': form,'cacHocPhan': cacHocPhan,'cacHocPhan': cacHocPhan,'cacHocPhanDuocChon': cacHocPhanDuocChon,'hocPhanDaDangKy': hocPhanDaDangKy,'cacHocPhanDuocChon': cacHocPhanDuocChon})

@login_required
def HuyDangKy(request, id):
    alert_content = 'Hủy'
    hocPhanDaDangKy = get_object_or_404(HocPhanDaDangKy, id=id)
    hocPhanDaDangKy.delete()
    url = reverse('listXetDuyetDangKy') + f'?alertContent={alert_content}'
    return redirect(url)


