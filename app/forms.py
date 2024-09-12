from app.models import *
from django import forms


class CollectionPlanForm(forms.ModelForm):
    class Meta:
        model = CollectionPlan
        fields = ['year', 'billing_period','payment_name','major','payment_amount','start_date','end_date','description']

class OtherCollectionPaymentForm(forms.ModelForm):
    class Meta:
        model = OtherCollectionPayment
        fields = ["student","other_collection_plan","end_date","detail","payment_amount"]

class BatchOtherCollectionPaymentForm(forms.ModelForm):
    class Meta:
        model = OtherCollectionPayment
        fields = ["other_collection_plan","end_date","detail","payment_amount"] 

class OtherCollectionPlanForm(forms.ModelForm):
    class Meta:
        model = OtherCollectionPlan
        fields = ['study_program','faculty','payment_name','description','payment_amount']

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['course_id','course_name','course_credit','payment_amount','study_program','major']
        widgets = {
            'major': forms.Select(attrs={'required': False}),
        }

class CourseAllowedForRegistrationForm(forms.ModelForm):
    class Meta:
        model = CourseAllowedForRegistration
        fields = ['course', 'class_year','enrollment_batch', 'semester','major','status']

class StudentClassForm(forms.ModelForm):
    class Meta:
        model = StudentClass
        fields = ['study_program','major','faculty','class_name','enrollment_batch']

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['student_id','student_name','birth_date','home_town','student_class','status','enrollment_batch']

class PaymentForm(forms.Form):
    order_id = forms.CharField(max_length=250)
    order_type = forms.CharField(max_length=20)
    amount = forms.IntegerField()
    order_desc = forms.CharField(max_length=100)
    bank_code = forms.CharField(max_length=20, required=False)
    language = forms.CharField(max_length=2)

class ExcelUploadForm(forms.Form):
    excel_file = forms.FileField()