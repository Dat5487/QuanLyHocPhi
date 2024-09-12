from django.shortcuts import render, redirect
from app.models import *
from app.forms import *
from django.contrib.auth import authenticate, login, logout, get_user_model


def register(request):
    student_id = "taichinh"
    password = "taichinh"
    CustomUser = get_user_model()
    user = CustomUser.objects.create_user(username=student_id, password=password,student_id=student_id,role="tai_chinh")
    user.save()
    return redirect(request, 'index.html')

def home(request):
    role = request.session.get('role')
    if role == 'student':
        return redirect('sinh_vien_home')
    elif role == 'dao_tao':
        return redirect('dao_tao_home')
    elif role == 'tai_chinh':
        return redirect('tai_chinh_home')
    return redirect('login')

def login_page(request):
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.role == 'TaiChinh':
                request.session['role'] = 'tai_chinh'
                return redirect('tai_chinh_home')
            elif user.role == 'DaoTao':
                request.session['role'] = 'dao_tao'
                return redirect('dao_tao_home')
            elif user.role == 'SinhVien':
                request.session['role'] = 'student'
                request.session['student_id'] = username
                return redirect('sinh_vien_home')
        else:
            return render(request, 'login/login.html', {'alert':"Error"})
    else:
        return render(request, 'login/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')



