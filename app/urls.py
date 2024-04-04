from django.urls import path
from app.views import *
from django.contrib.auth.decorators import login_required

urlpatterns = [
    
   path('addGenesis/', add_block, name="addGenesis"),
   path('register/', register, name="register"),
   path('login/', login_page, name='login'),
   path('logout/', logout_view, name='logout'),

   #---------------------------------------------------------------------------
   #--------------------------------Cán Bộ-------------------------------------
   #---------------------------------------------------------------------------
   path('canBoHome', CanBoHome,name="canBoHome"),

   path('listThietLapDangKy/', login_required(ListThietLapDangKy), name="listThietLapDangKy"),
   path('thietLapDangKy/<int:id>/detail/', login_required(XemThietLapDangKy), name='xemThietLapDangKy'),
   path('thietLapDangKy/newThietLapDangKy/', login_required(NewThietLapDangKy), name='newThietLapDangKy'),
   path('thietLapDangKy/<int:id>/update/', login_required(SuaThietLapDangKy), name='suaThietLapDangKy'),
   path('thietLapDangKy/<int:id>/delete/', login_required(XoaThietLapDangKy), name='xoaThietLapDangKy'),

   path('listXetDuyetDangKy/', login_required(ListXetDuyetDangKy), name="listXetDuyetDangKy"),
   path('xetDuyetDangKy/<int:id>', login_required(XetDuyetDangKy), name="xetDuyetDangKy"),
   path('huyDangKy/<int:id>', login_required(HuyDangKy), name="huyDangKy"),

   #-----------------------------------------------------------------------------
   #-------------------------------Tài Chính-------------------------------------
   #-----------------------------------------------------------------------------

   path('taiChinhHome', taiChinhHome,name="taiChinhHome"),
   path('listinvalidblocks/', login_required(ListInvalidBlocks), name="listInvalidBlocks"),
   path('chonbaocao/', login_required(ChonBaoCao), name="chonBaoCao"),

   path('listKeHoachThu/', login_required(ListKeHoachThu), name="listKeHoachThu"),
   path('kehoachthu/<int:id>/detail/', login_required(XemKeHoachThu), name='xemKeHoachThu'),
   path('kehoachthu/newKeHoachThu/', login_required(NewKeHoachThu), name='newKeHoachThu'),
   path('kehoachthu/<int:id>/update/', login_required(SuaKeHoachThu), name='suaKeHoachThu'),
   path('kehoachthu/<int:id>/delete/', login_required(XoaKeHoachThu), name='xoaKeHoachThu'),

   path('listLop/', login_required(ListLop), name="listLop"),
   path('listSinhVien/<int:id>/', login_required(ListSinhVien), name="listSinhVien"),
   path('listLichSuThanhToan/<int:id>/', login_required(ListLichSuThanhToan), name="listLichSuThanhToan"),
   path('xemcackhoanthu/<int:id>/', login_required(XemCacKhoanThuCuaSV), name='xemCacKhoanThuSV'),

   path('newThanhToanKhac/<int:id>/', login_required(NewThanhToanKhoanThuKhac), name='newThanhToanKhoanThuKhac'),
   path('addThanhToanKhac/<int:id>/', login_required(AddThanhToanKhoanThuKhac), name='addThanhToanKhoanThuKhac'),
   path('thanhToanKhac/<int:id>/detail/', login_required(XemThanhToanKhoanThuKhac), name='xemThanhToanKhoanThuKhac'),
   path('thanhToanKhac/<int:id>/delete/', login_required(XoaThanhToanKhoanThuKhac), name='xoaThanhToanKhoanThuKhac'),
   # path('thanhToanKhac/<int:id>/update/', login_required(SuaThanhToanKhoanThuKhac), name='suaThanhToanKhoanThuKhac'),

   path('khoanthuhocphi/<int:id>/detail/', login_required(XemKhoanThuHocPhi), name='xemKhoanThuHocPhi'),

   path('listKhoanThuKhac/', login_required(ListKhoanThuKhac), name="listKhoanThuKhac"),
   path('khoanThuKhac/newKhoanThuKhac/', login_required(NewKhoanThuKhac), name='newKhoanThuKhac'),
   path('khoanThuKhac/<int:id>/update/', login_required(SuaKhoanThuKhac), name='suaKhoanThuKhac'),
   path('khoanThuKhac/<int:id>/delete/', login_required(XoaKhoanThuKhac), name='xoaKhoanThuKhac'),

   #-----------------------------------------------------------------------------
   #-------------------------------Sinh viên-------------------------------------
   #-----------------------------------------------------------------------------

   path('sinhVienHome/', sinhVienHome, name='sinhVienHome'),
   path('dangKyTinChi/', login_required(DangKyTinChi), name='dangKyTinChi'),
   path('hocPhanDaDangKy/', login_required(ListHocPhanDaDangKy), name='hocPhanDaDangKy'),

   path('listKhoanThanhToan/', login_required(ListKhoanThanhToan), name='listKhoanThanhToan'),
   path('xemThanhToanHocPhi/<int:id>/', login_required(XemThanhToanHocPhi), name='xemThanhToanHocPhi'),
   path('xemThanhToanKhac/<int:id>/', login_required(XemThanhToanKhac), name='xemThanhToanKhac'),
   path('taoMaThanhToanHocPhi/<int:id>/', login_required(TaoMaThanhToanHocPhi), name='taoMaThanhToanHocPhi'),
   path('taoMaThanhToanKhac/<int:id>/', login_required(TaoMaThanhToanKhac), name='taoMaThanhToanKhac'),

   path('pay', index, name='pay'),
   path('payment/<str:id>', payment, name='payment'),
   path('payment_ipn', payment_ipn, name='payment_ipn'),
   path('payment_return', payment_return, name='payment_return'),
   path('query', query, name='query'),
   path('refund', refund, name='refund'),

]