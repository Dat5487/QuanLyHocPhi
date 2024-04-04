from django.shortcuts import render, redirect
from app.models import *
from app.forms import *
from django.contrib.auth import authenticate, login, logout, get_user_model

def register(request):
    maSinhVien = "dat548712"
    password = "123456"
    # Create a new user
    CustomUser = get_user_model()

    user = CustomUser.objects.create_user(username=maSinhVien, password=password,maSinhVien=maSinhVien,role="user")
    user.save()

    # Redirect to a success page or login page
    return redirect(request, 'index.html')

def login_page(request):
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.role == 'TaiChinh':
                return redirect('taiChinhHome')
            elif user.role == 'CanBo':
                return redirect('canBoHome')
            elif user.role == 'SinhVien':
                request.session['maSinhVien'] = username
                return redirect('sinhVienHome')
        else:
            return render(request, 'login/login.html', {'alert':"Error"})
    else:
        return render(request, 'login/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')



