from django.urls import path
from app.views import *
from django.contrib.auth.decorators import login_required

urlpatterns = [
    
   path('addGenesis/', add_block, name="addGenesis"),
   path('register/', register, name="register"),
   path('login/', login_page, name='login'),
   path('logout/', logout_view, name='logout'),
   path('', home, name='home'),

   #---------------------------------------------------------------------------
   #-------------------------Cán Bộ phòng đào tạo------------------------------
   #---------------------------------------------------------------------------
   path('dao_tao_home', DaoTaoHome,name="dao_tao_home"),

   path('course_registration_preset_list/', login_required(RegistrationPresetList), name="course_registration_preset_list"),
   path('registration_preset/<int:id>/detail/', login_required(RegistrationPresetDetail), name='detail_preset'),
   path('registration_preset/new_preset/', login_required(CreateRegistrationPreset), name='new_preset'),
   path('registration_preset/<int:id>/update/', login_required(EditRegistrationPreset), name='edit_preset'),
   path('registration_preset/<int:id>/delete/', login_required(DeleteRegistrationPreset), name='delete_preset'),

   path('course_registration_approval/', login_required(PendingRegistrationsList), name="course_registration_approval"),
   path('approve_registration/<int:id>', login_required(CourseRegistrationApproval), name="approve_registration"),
   path('course_registration_denied/<int:id>', login_required(CourseRegistrationDenied), name="course_registration_denied"),

   path('major_drop_list/', login_required(MajorDropList), name="major_drop_list"),
   path('class_list/<int:id>/', login_required(ClassList), name="class_list"),
   path('new_class/<int:id>/', login_required(CreateClass), name="new_class"),
   path('delete_class/<int:id>/', login_required(DeleteClass), name="delete_class"),

   path('class_student_list/<int:id>/', login_required(ClassStudentList), name="class_student_list"),
   path('detail_student/<int:id>/', login_required(DetailStudent), name="detail_student"),
   path('create_student/<int:id>/', login_required(CreateStudent), name="create_student"),
   path('edit_student/<int:id>/', login_required(EditStudent), name="edit_student"),
   path('delete_student/<int:id>/', login_required(DeleteStudent), name="delete_student"),

   path('course_list/', login_required(CourseList), name="course_list"),
   path('course/new_course/', login_required(NewCourse), name='new_course'),
   path('course/<int:id>/update/', login_required(EditCourse), name='edit_course'),
   path('course/<int:id>/delete/', login_required(DeleteCourse), name='delete_course'),

   path('excel_import_students/<int:id>/', login_required(ExcelImportStudents), name="excel_import_students"),
   path('excel_import_courses/', login_required(ExcelImportCourses), name="excel_import_courses"),

   #-----------------------------------------------------------------------------
   #-------------------------------Tài Chính-------------------------------------
   #-----------------------------------------------------------------------------

   path('tai_chinh_home', tai_chinh_home,name="tai_chinh_home"),
   path('invalid_block_list/', login_required(InvalidBlockList), name="invalid_block_list"),
   path('select_report/', login_required(SelectReport), name="select_report"),

   path('plan_list/', login_required(CollectionPlanList), name="plan_list"),
   path('collection_plan/<int:id>/detail/', login_required(CollectionPlanDetail), name='collection_plan_detail'),
   path('collection_plan/new_collection_plan/', login_required(NewCollectionPlan), name='new_collection_plan'),
   path('collection_plan/<int:id>/update/', login_required(EditCollectionPlan), name='edit_collection_plan'),
   path('collection_plan/<int:id>/delete/', login_required(DeleteCollectionPlan), name='delete_collection_plan'),

   path('class_list/', login_required(SelectClassDropdown), name="class_list"),
   path('student_list/<int:id>/', login_required(StudentList), name="student_list"),
   path('tuition_payment_list/<int:id>/', login_required(TuitionPaymentList), name="tuition_payment_list"),
   path('student_tuition_list/<int:id>/', login_required(StudentTuitionList), name='student_tuition_list'),

   path('add_plan/<int:id>/', login_required(AddOtherCollectionPayment), name='add_plan'),
   path('batch_add_plan/<int:id>/', login_required(BatchCreateOtherCollectionPlan), name='batch_add_plan'),
   path('other_tuition_payment/<int:id>/detail/', login_required(DetailOtherCollectionPayment), name='other_collection_payment_detail'),
   path('other_tuition_payment/<int:id>/delete/', login_required(DeleteOtherCollectionPayment), name='delete_other_collection_payment'),
   # path('other_tuition_payment/<int:id>/update/', login_required(EditOtherCollectionPayment), name='edit_other_collection_payment'),

   path('student_payment/<int:id>/detail/', login_required(StudentPayment), name='student_payment'),

   path('preset_list/', login_required(OtherCollectionPlanList), name="preset_list"),
   path('other_collection_plan/create_plan_preset/', login_required(CreateOtherCollectionPlan), name='create_plan_preset'),
   path('other_collection_plan/<int:id>/update/', login_required(EditOtherCollectionPlan), name='edit_plan_preset'),
   path('other_collection_plan/<int:id>/delete/', login_required(DeleteOtherCollectionPlan), name='delete_plan_preset'),



   #-----------------------------------------------------------------------------
   #-------------------------------Sinh viên-------------------------------------
   #-----------------------------------------------------------------------------

   path('sinh_vien_home/', sinh_vien_home, name='sinh_vien_home'),
   path('course_registration/', login_required(CourseRegistration), name='course_registration'),
   path('registed_course/', login_required(RegisteredCourse), name='registed_course'),

   path('payment_list/', login_required(PaymentList), name='payment_list'),
   path('tuition_detail/<int:id>/', login_required(TuitionDetail), name='tuition_detail'),
   path('other_tuition_detail/<int:id>/', login_required(OtherTuitionDetail), name='other_tuition_detail'),
   path('tuition_payment_id/<int:id>/', login_required(CreateTuitionPaymentID), name='tuition_payment_id'),
   path('other_tuition_payment_id/<int:id>/', login_required(CreateOtherTuitionPaymentID), name='other_tuition_payment_id'),

   path('pay', index, name='pay'),
   path('payment/<str:id>', payment, name='payment'),
   path('payment_ipn', payment_ipn, name='payment_ipn'),
   path('payment_return', payment_return, name='payment_return'),
   path('query', query, name='query'),
   path('refund', refund, name='refund'),

]