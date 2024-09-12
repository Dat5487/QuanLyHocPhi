from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from app.models import *
from app.forms import *
from django.contrib.auth.decorators import login_required
import pandas as pd
from django.contrib.auth import  get_user_model
from django.db.models import ProtectedError

@login_required
def DaoTaoHome(request):
   registration_preset_count = CourseAllowedForRegistration.objects.filter(status = True).count()
   pending_registration_count = RegistedCourse.objects.filter(status = False).count()
   return render(request, 'dao_tao/dao_tao_home.html', {'registration_preset_count': registration_preset_count, 'pending_registration_count': pending_registration_count})

@login_required
def RegistrationPresetList(request):
   alert_content = request.GET.get('alert_content')
   preset_list = CourseAllowedForRegistration.objects.all().order_by('-id')
   return render(request, 'dao_tao/course_registration_preset/preset_list.html', {'preset_list': preset_list, 'alert_content': alert_content})

@login_required
def RegistrationPresetDetail(request, id):
   alert_content = request.GET.get('alert_content')
   all_preset = get_object_or_404(CourseAllowedForRegistration, id=id).course.all()
   total_course_credit = sum(course.course_credit for course in all_preset)
   total_payment_amount = sum(course.payment_amount for course in all_preset)
   registration_preset = get_object_or_404(CourseAllowedForRegistration, id=id)

   if request.method == 'POST':
        registration_preset.status = request.POST.get('status')
        registration_preset.save()
        alert_content = 'Edit'
        url = reverse('course_registration_preset_list') + f'?alert_content={alert_content}'
        return redirect(url)

   return render(request, 'dao_tao/course_registration_preset/detail_preset.html', {'all_preset': all_preset, 'total_payment_amount': total_payment_amount, 'total_course_credit': total_course_credit, 'alert_content': alert_content,'registration_preset' : registration_preset})


@login_required
def CreateRegistrationPreset(request):
    study_programs = StudyProgram.objects.all().order_by('-id')
    faculties = Faculty.objects.all().order_by('-id')
    majors = Major.objects.all().order_by('-id')
    class_years = ClassYear.objects.all().order_by('-id')
    courses = Course.objects.all().order_by('-id')
    if request.method == 'POST':
        form = CourseAllowedForRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            alert_content = 'Create'
            url = reverse('course_registration_preset_list') + f'?alert_content={alert_content}'
            return redirect(url)
    else:
        form = CourseAllowedForRegistrationForm()
    return render(request, 'dao_tao/course_registration_preset/new_preset.html', {'form': form, 'courses': courses, 'class_years': class_years, 'study_programs': study_programs, 'faculties': faculties, 'majors': majors})

@login_required
def EditRegistrationPreset(request, id):
    registration_preset = get_object_or_404(CourseAllowedForRegistration, id=id)
    selected_courses = registration_preset.course.all()
    majors = Major.objects.all().order_by('-id')
    class_years = ClassYear.objects.all().order_by('-id')
    courses = Course.objects.all().order_by('-id')
    if request.method == 'POST':
        registration_preset.class_year = get_object_or_404(ClassYear, id=request.POST.get('class_year'))
        registration_preset.enrollment_batch = request.POST.get('enrollment_batch')
        registration_preset.semester = request.POST.get('semester')
        
        course_ids = request.POST.getlist('course')
        course_objects = Course.objects.filter(id__in=course_ids)
        registration_preset.course.set(course_objects)
        
        registration_preset.status = request.POST.get('status')
        registration_preset.save()
        alert_content = 'Edit'
        url = reverse('course_registration_preset_list') + f'?alert_content={alert_content}'
        return redirect(url)
    else:
        form = CourseAllowedForRegistrationForm()
    return render(request, 'dao_tao/course_registration_preset/edit_preset.html', {'form': form,'class_years': class_years,'courses': courses,'registration_preset': registration_preset,'majors': majors,'selected_courses': selected_courses})

#####
@login_required
def DeleteRegistrationPreset(request, id):
    registration_preset = get_object_or_404(CourseAllowedForRegistration, id=id)
    all_preset = registration_preset.course.all()
    total_course_credit = sum(course.course_credit for course in all_preset)
    total_payment_amount = sum(course.payment_amount for course in all_preset)
    if request.method == 'POST':
        try:
            registration_preset.delete()
            alert_content = 'Delete'
            url = reverse('course_registration_preset_list') + f'?alert_content={alert_content}'
            return redirect(url)
        except ProtectedError:
            return render(request, 'error.html')

    return render(request, 'dao_tao/course_registration_preset/delete_preset.html', {'registration_preset': registration_preset,'total_course_credit':total_course_credit,'total_payment_amount':total_payment_amount})


@login_required
def PendingRegistrationsList(request):
   alert_content = request.GET.get('alert_content')
   pending_registrations = RegistedCourse.objects.all().filter(status = 0).order_by('-id')
   return render(request, 'dao_tao/course_registration_approval/pending_registrations.html', {'pending_registrations': pending_registrations, 'alert_content': alert_content})

@login_required
def CourseRegistrationApproval(request, id):
    registed_course = get_object_or_404(RegistedCourse, id=id)
    selected_courses = registed_course.course.all()
    courses = registed_course.course_allowed_for_registration.course.all()
    if request.method == 'POST':
        registed_course.status = 1
        registed_course.save()
        approved_course = ApprovedCourse(registed_course=registed_course)
        approved_course.save()
        payment_amount =  sum(course.payment_amount for course in registed_course.course.all())
        course_credit =  sum(course.course_credit for course in registed_course.course.all())
        tuition_payment = TuitionPayment(approved_course=approved_course,student = registed_course.student,payment_amount = payment_amount, course_credit=course_credit, status = 0 , created_date = None )
        tuition_payment.save()
        alert_content = 'Approved'
        url = reverse('course_registration_approval') + f'?alert_content={alert_content}'
        return redirect(url)
    else:
        form = CourseAllowedForRegistrationForm()
    return render(request, 'dao_tao/course_registration_approval/approve_registration.html', {'form': form,'courses': courses,'courses': courses,'selected_courses': selected_courses,'registed_course': registed_course,'selected_courses': selected_courses})

@login_required
def CourseRegistrationDenied(request, id):
    alert_content = 'Denied'
    registed_course = get_object_or_404(RegistedCourse, id=id)
    registed_course.delete()
    url = reverse('course_registration_approval') + f'?alert_content={alert_content}'
    return redirect(url)


@login_required
def MajorDropList(request):
   study_programs = StudyProgram.objects.all().order_by('-id')
   faculties = Faculty.objects.all().order_by('-id')
   majors = Major.objects.all().order_by('-id')
   return render(request, 'dao_tao/student_management/major_drop_list.html', {'study_programs': study_programs,'faculties': faculties,'majors': majors})

@login_required
def ClassList(request, id):
    alert_content = request.GET.get('alert_content')
    major = get_object_or_404(Major, id=id)
    class_list = StudentClass.objects.filter(major = id).order_by('-id')
    return render(request, 'dao_tao/class_management/class_list.html', {'class_list': class_list,'major':major,'alert_content':alert_content})

@login_required
def CreateClass(request,id):
    major = get_object_or_404(Major, id=id)
    if request.method == 'POST':
        form = StudentClassForm(request.POST)
        if form.is_valid():
            form.save()
            alert_content = 'Create'
            url = reverse('class_list', args=[id]) + f'?alert_content={alert_content}'
            return redirect(url)
    else:
        form = StudentClassForm()
    return render(request, 'dao_tao/class_management/new_class.html', {'form': form, 'major': major})

@login_required
def DeleteClass(request, id):
    class_name = get_object_or_404(StudentClass, id=id)
    idNganhDaoTao = class_name.major.id
    if request.method == 'POST':
        try:
            class_name.delete()
            alert_content = 'Delete'
            url = reverse('class_list', args=[idNganhDaoTao]) + f'?alert_content={alert_content}'
            return redirect(url)
        except ProtectedError:
            return render(request, 'error.html')

    return render(request, 'dao_tao/class_management/delete_class.html', {'class_name': class_name})

@login_required
def ClassStudentList(request, id):
   alert_content = request.GET.get('alert_content')
   student_class = get_object_or_404(StudentClass, id=id)
   student_list = Student.objects.filter(id = id).order_by('-id')
   return render(request, 'dao_tao/student_management/class_student_list.html', {'student_list': student_list,'student_class':student_class,'alert_content':alert_content})

@login_required
def DetailStudent(request, id):
   student = get_object_or_404(Student, id=id)
   student_list = Student.objects.filter(class_name = id).order_by('-id')
   return render(request, 'dao_tao/student_management/detail_student.html', {'student': student,'student_list':student_list})

@login_required
def CreateStudent(request,id):
    class_name = get_object_or_404(StudentClass, id=id)
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            student_id = request.POST.get('student_id')
            custom_user = get_user_model()
            user = custom_user.objects.create_user(username=student_id, password=student_id,student_id=student_id,role="Student")
            user.save()
            alert_content = 'Create'
            url = reverse('student_list', args=[id]) + f'?alert_content={alert_content}'
            return redirect(url)
    else:
        form = StudentForm()
    return render(request, 'dao_tao/student_management/new_student.html', {'form': form, 'class_name': class_name})

@login_required
def EditStudent(request, id):
    student = get_object_or_404(Student, id=id)
    class_id = student.student_class.id
    class_list = StudentClass.objects.all().order_by('-id')
    if request.method == 'POST':
        student.student_class = get_object_or_404(StudentClass, id=request.POST.get('class_name'))
        student.gender = request.POST.get('gender')
        student.home_town = request.POST.get('home_town')
        student.birth_date = request.POST.get('birth_date')
        student.status = request.POST.get('status')
        student.save()
        alert_content = 'Edit'
        url = reverse('student_list',args=[class_id]) + f'?alert_content={alert_content}'
        return redirect(url)
    else:
        form = StudentForm()
    return render(request, 'dao_tao/student_management/edit_student.html', {'form': form,'class_list': class_list,'student':student})


@login_required
def DeleteStudent(request, id):
    student = get_object_or_404(Student, id=id)
    class_id = student.student_class.id
    if request.method == 'POST':
        try:
            student.delete()
            user = get_object_or_404(CustomUser, username = student.student_id)
            user.delete()
            alert_content = 'Delete'
            url = reverse('student_list', args=[class_id]) + f'?alert_content={alert_content}'
            return redirect(url)
        except ProtectedError:
            return render(request, 'error.html')

    return render(request, 'dao_tao/student_management/delete_student.html', {'student': student})

def ExcelImportStudents(request,id):
    excel_file = request.FILES['excel_file']
    df = pd.read_excel(excel_file)
    class_name = get_object_or_404(StudentClass, id=id)
    for index, row in df.iterrows():
        obj = Student() 
        student_id = row['Mã sinh viên']
        obj.student_id = student_id
        obj.student_name = row['Họ tên']
        obj.gender = row['Giới tính']
        obj.home_town = row['Quê quán']
        obj.birth_date = row['Ngày sinh']
        obj.enrollment_batch = class_name.enrollment_batch
        obj.class_name = class_name
        obj.status = 1
        obj.save()
        CustomUser = get_user_model()
        user = CustomUser.objects.create_user(username=student_id, password=student_id,student_id=student_id,role="Student")
        user.save()
    alert_content = 'Create'
    url = reverse('student_list',args=[id]) + f'?alert_content={alert_content}'
    return redirect(url)

def ExcelImportCourses(request):
    excel_file = request.FILES['excel_file']
    df = pd.read_excel(excel_file)
    for index, row in df.iterrows():
        obj = Course() 
        obj.study_program = get_object_or_404(StudyProgram, study_program_name = row['Hệ đào tạo'])
        major = row['Ngành đào tạo']
        major = major if pd.notna(major) else None
        print(major)
        if major is not None:
            obj.major = get_object_or_404(Major, major_name= major)
        else:
            obj.major = None
        obj.course_id = row['Mã học phần']
        obj.course_name = row['Tên học phần']
        obj.course_credit = row['Số tín chỉ']
        obj.payment_amount = row['Số tiền']
        obj.save()
    alert_content = 'Create'
    url = reverse('course_list') + f'?alert_content={alert_content}'
    return redirect(url)

@login_required
def CourseList(request):
   alert_content = request.GET.get('alert_content')
   course_list = Course.objects.all().order_by('-id')
   faculties = Faculty.objects.all().order_by('-id')
   majors = Major.objects.all().order_by('-id')
   study_programs = StudyProgram.objects.all().order_by('-id')
   return render(request, 'dao_tao/course_management/course_list.html', {'course_list': course_list,'alert_content': alert_content, 'study_programs': study_programs,'faculties': faculties,'majors': majors})

@login_required
def NewCourse(request):
    faculties = Faculty.objects.all().order_by('-id')
    majors = Major.objects.all().order_by('-id')
    study_programs = StudyProgram.objects.all().order_by('-id')
    if request.method == 'POST':
        form = CourseForm(request.POST)
        data_copy = request.POST.copy()
        data_copy['payment_amount'] = data_copy['payment_amount'].replace(",", "") 
        form.data = data_copy
        if form.is_valid():
            form.save()
            alert_content = 'Create'
            url = reverse('course_list') + f'?alert_content={alert_content}'
            return redirect(url)
    else:
        form = CourseForm()
    return render(request, 'dao_tao/course_management/new_course.html', {'form': form, 'study_programs': study_programs,'faculties': faculties,'majors': majors})

@login_required
def EditCourse(request, id):
    course = get_object_or_404(Course, id=id)
    payment_amount = format(course.payment_amount, ",.0f")

    if request.method == 'POST':
        course.payment_amount = request.POST.get('payment_amount').replace(",", "")
        course.course_name = request.POST.get('course_name')
        course.course_credit = request.POST.get('course_credit')
        course.save()
        alert_content = 'Edit'
        url = reverse('course_list') + f'?alert_content={alert_content}'
        return redirect(url)
    else:
        course = Course.objects.get(id=id)
        form = CourseForm()
    return render(request, 'dao_tao/course_management/edit_course.html', {'form': form,'course': course,'payment_amount':payment_amount})

@login_required
def DeleteCourse(request, id):
    course = get_object_or_404(Course, id=id)
    payment_amount = format(course.payment_amount, ",.0f")
    if request.method == 'POST':
        try:
            course.delete()
            alert_content = 'Delete'
            url = reverse('course_list') + f'?alert_content={alert_content}'
            return redirect(url)
        except ProtectedError:
            return render(request, 'error.html')

    return render(request, 'dao_tao/course_management/delete_course.html', {'course': course, 'payment_amount': payment_amount})