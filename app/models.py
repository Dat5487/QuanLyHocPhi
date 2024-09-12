from django.db import models
from django.contrib.auth.models import AbstractUser

class StudyProgram(models.Model):
    study_program_name = models.CharField(max_length=50)

# Khóa nhập học
class Year(models.Model):
    year = models.CharField(max_length=10)

# Năm học
class ClassYear(models.Model):
    class_year = models.CharField(max_length=10)

class Faculty(models.Model):
    faculty_name = models.CharField(max_length=50)
    
class Major(models.Model):
    faculty = models.ForeignKey(Faculty, on_delete = models.PROTECT)
    study_program = models.ForeignKey(StudyProgram, on_delete = models.PROTECT)
    major_name = models.CharField(max_length=50)

class StudentClass(models.Model):
    study_program = models.ForeignKey(StudyProgram, on_delete = models.PROTECT)
    major = models.ForeignKey(Major, on_delete = models.PROTECT)
    faculty = models.ForeignKey(Faculty, on_delete = models.PROTECT)
    class_name = models.CharField(max_length=50)
    enrollment_batch = models.IntegerField()

    
class Student(models.Model):
    student_id = models.CharField(max_length=10)
    student_name = models.CharField(max_length=50)
    gender = models.CharField(max_length=5,null=True)
    birth_date = models.DateField(blank=True, null=True)
    home_town = models.CharField(max_length=50)
    student_class = models.ForeignKey(StudentClass, on_delete = models.PROTECT)
    status = models.BooleanField(blank=True)
    enrollment_batch = models.IntegerField()
    
class OtherCollectionPlan(models.Model):
    study_program = models.ForeignKey(StudyProgram, on_delete = models.PROTECT, blank=True, null=True)
    faculty = models.ForeignKey(Faculty, on_delete = models.PROTECT, blank=True, null=True)
    payment_name = models.CharField(max_length=100)
    payment_amount = models.BigIntegerField()
    description = models.TextField(blank=True, null=True)

class OtherCollectionPayment(models.Model):
    other_collection_plan = models.ForeignKey(OtherCollectionPlan, on_delete = models.PROTECT)
    student = models.ForeignKey(Student, on_delete = models.PROTECT)
    status = models.BooleanField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    detail = models.CharField(max_length=100,blank=True, null=True)
    payment_amount = models.BigIntegerField()
    added_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)

class CollectionPlan(models.Model):
    year = models.ForeignKey(Year, on_delete = models.PROTECT)
    billing_period = models.IntegerField()
    major = models.ForeignKey(Major, on_delete = models.PROTECT)
    payment_name = models.CharField(max_length=100)
    status = models.BooleanField(blank=True, null=True)
    payment_amount = models.BigIntegerField()
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)

class CustomUser(AbstractUser):
    # Add any additional fields you need for your user model
    student_id = models.TextField()
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
    student_id = models.TextField()
    payment_id = models.TextField()
    payment_amount = models.BigIntegerField()
    description = models.TextField(blank=True, null=True)
    transaction_id = models.BigIntegerField()
    result = models.TextField()
    previous_hash = models.CharField(max_length=256)
    hash = models.CharField(max_length=256)
    nonce = models.IntegerField()

class Course(models.Model):
    course_id = models.TextField()
    course_name = models.TextField()
    course_credit = models.IntegerField()
    payment_amount = models.IntegerField()
    study_program = models.ForeignKey(StudyProgram, on_delete = models.PROTECT, null=True)
    major = models.ForeignKey(Major, on_delete = models.PROTECT, blank=True, null=True)

class CourseAllowedForRegistration(models.Model):
    course = models.ManyToManyField(Course)
    class_year = models.ForeignKey(ClassYear, on_delete = models.PROTECT)
    enrollment_batch = models.IntegerField()
    semester = models.BooleanField(blank=True)
    major = models.ForeignKey(Major, on_delete = models.PROTECT)
    status = models.BooleanField(blank=True)

class RegistedCourse(models.Model):
    course_allowed_for_registration = models.ForeignKey(CourseAllowedForRegistration, on_delete = models.PROTECT)
    course = models.ManyToManyField(Course)
    student = models.ForeignKey(Student, on_delete = models.PROTECT)
    class_year = models.ForeignKey(ClassYear, on_delete = models.PROTECT)
    enrollment_batch = models.IntegerField()
    semester = models.BooleanField(blank=True)
    status = models.BooleanField(blank=True)

class ApprovedCourse(models.Model):
    registed_course = models.ForeignKey(RegistedCourse, on_delete = models.PROTECT)

class TuitionPayment(models.Model):
    approved_course = models.ForeignKey(ApprovedCourse, on_delete = models.PROTECT)
    student = models.ForeignKey(Student, on_delete = models.PROTECT)
    payment_amount = models.BigIntegerField()
    course_credit = models.IntegerField()
    status = models.BooleanField(blank=True)
    created_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)

