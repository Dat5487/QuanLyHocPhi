from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from app.models import *
from app.forms import *
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect


@login_required
def sinh_vien_home(request):
    student_id = request.session.get('student_id')
    student = get_object_or_404(Student, student_id=student_id)
    student_name = student.student_name
    total_tuition_amount = TuitionPayment.objects.filter(student = student).filter(status = False).count()
    total_other_tuition_amount = OtherCollectionPayment.objects.filter(student = student).filter(status = False).count()

    return render(request, 'sinh_vien/sinh_vien_home.html', {'student_name': student_name,'total_tuition_amount':total_tuition_amount,'total_other_tuition_amount':total_other_tuition_amount})


@login_required
def CourseRegistration(request):
    alert_content = request.GET.get('alert_content')
    student_id = request.session.get('student_id')
    student = get_object_or_404(Student, student_id=student_id)
    registration_preset = CourseAllowedForRegistration.objects.all().filter(enrollment_batch=student.enrollment_batch, major=student.student_class.major, status = 1).order_by('-id').first()
    registed_course = RegistedCourse.objects.all().filter(course_allowed_for_registration=registration_preset, student = student).order_by('-id').first()
    approved_course = ApprovedCourse.objects.filter(registed_course = registed_course).first()
    if approved_course is None and registration_preset is not None:
        if registed_course is not None:
            selected_courses = registed_course.course.all()
        else:
            selected_courses = None

        if registration_preset is not None:
            courses = registration_preset.course.all()
        else:
            registration_preset = None
            courses = None
    else:
        return render(request, 'sinh_vien/course_registration/course_registration.html', {'status': False})

    if request.method == 'POST':
        course_ids = request.POST.getlist('course')  # Retrieve a list of selected course IDs
        courses = Course.objects.filter(id__in=course_ids)  # Retrieve the corresponding Course objects
        
        if registed_course is not None:
            registed_course.course.set(courses)
            registed_course.save()
        else:
            registed_course = RegistedCourse(course_allowed_for_registration=registration_preset, student=student, class_year=registration_preset.class_year, enrollment_batch = registration_preset.enrollment_batch, semester= registration_preset.semester,status = 0)
            registed_course.save()
            registed_course.course.set(courses)
            registed_course.save()
        
        alert_content = 'register'
        url = reverse('course_registration') + f'?alert_content={alert_content}'
        return redirect(url)
    else:
        form = CourseAllowedForRegistrationForm()
    return render(request, 'sinh_vien/course_registration/course_registration.html', {'form': form,'registration_preset': registration_preset,'courses': courses,'selected_courses': selected_courses,'alert_content':alert_content})


@login_required
def RegisteredCourse(request):
    student_id = request.session.get('student_id')
    student = get_object_or_404(Student, student_id=student_id)
    approved_courses = ApprovedCourse.objects.all().filter(registed_course__student=student).order_by('-id')
    registed_courses = []
    for item in approved_courses:
        registed_courses.append(item.registed_course)
    return render(request, 'sinh_vien/registered_course/registered_course_list.html', {'registed_courses': registed_courses})

class Tuition:
    def __init__(self,id, class_year, semester, course_credit, payment_amount, status):
        self.id = id
        self.class_year = class_year
        self.semester = semester
        self.course_credit = course_credit
        self.payment_amount = payment_amount
        self.status = status

@login_required
def PaymentList(request):
    student_id = request.session.get('student_id')
    student = get_object_or_404(Student, student_id=student_id)
    payments = TuitionPayment.objects.all().filter(student=student)
    payment_list = []
    for payment in payments:
        course_list = payment.approved_course.registed_course.course.all()
        id = payment.id
        class_year = payment.approved_course.registed_course.class_year.class_year
        semester = payment.approved_course.registed_course.semester
        course_credit =  sum(course.course_credit for course in course_list)
        payment_amount =  sum(course.payment_amount for course in course_list)
        status = payment.status
        extracted_payment = Tuition(id,class_year,semester,course_credit,payment_amount,status)
        payment_list.append(extracted_payment)
    other_payment_list = OtherCollectionPayment.objects.all().filter(student=student).order_by('-id')
    return render(request, 'sinh_vien/tuition_payment/tuition_list.html', {'payment_list': payment_list,'other_payment_list': other_payment_list})

@login_required
def TuitionDetail(request,id):
    tuition_payment = get_object_or_404(TuitionPayment,id = id)
    return render(request, 'sinh_vien/tuition_payment/tuition_detail.html', {'tuition_payment': tuition_payment})



@login_required
def OtherTuitionDetail(request,id):
    other_tuition_payment = get_object_or_404(OtherCollectionPayment,id = id)
    return render(request, 'sinh_vien/tuition_payment/other_tuition_detail.html', {'other_tuition_payment': other_tuition_payment})
