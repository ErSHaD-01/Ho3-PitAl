from django.urls import path
from . import views


urlpatterns = [
    path('' , views.home , name = 'home'),

    #<--- register/login/profile --->#
    path('accounts/register' , views.register_patient , name = 'register_patient'),
    path('accounts/login' , views.login , name = 'login'),
    path('accounts/logout' , views.logout , name = 'logout'),
    path('accounts/profile' , views.profile , name = 'profile'),
    path('accounts/edit/profile' , views.edit_profile , name = 'edit_profile'),
    #<--- endregister/login/profile --->#
    
    #<--- history --->#
    path('accounts/profile/history/<int:patient_id>' , views.history , name = 'history'),
    path('accounts/profile/disease/history/<int:patient_id>' , views.disease_history , name = 'disease_history'),
    path('accounts/profile/visit/history/<int:patient_id>' , views.visit_history , name = 'visit_history'),
    #<--- endhistory --->#

    #<--- visit --->#
    path('accounts/profile/visites/<int:patient_id>' , views.visits , name = 'visits'),
    path('accounts/profile/visites/data/<int:visit_id>' , views.visit_data , name = 'visit_data'),
    path('accounts/profile/visites/delete/<int:visit_id>' , views.visit_delete , name = 'visit_delete'),
    path('accounts/profile/create/visite/<int:patient_id>' , views.create_visit , name = 'create_visit'),
    #<--- endvisit --->#

    #<--- patient_detail --->#
    path('accounts/profile/patients' , views.show_patient , name = 'patient'),
    path('accounts/profile/patients/<int:patient_id>/' , views.patient_detail , name = 'patient_detail'),
    #<--- endpatient_detail --->#

    #<--- accept_visit --->#
    path('accounts/profile/my/visites/<int:doctor_id>/' , views.doctor_visit , name = 'doctor_visit'),
    path('accounts/profile/my/visites/data/<int:visit_id>/' , views.doctor_visit_data , name = 'doctor_visit_data'),
    #<--- endaccep_tvisit --->#
 
    #<--- prescription ---># 
    path('accounts/profile/prescriptions' , views.show_prescription , name = 'show_prescription'),
    path('accounts/profile/prescriptions/detail/<int:prescription_id>/' , views.prescription_detail , name = 'prescription_detail'),
    path('accounts/profile/prescription/<int:doctor_id>/' , views.show_patient_prescription , name = 'show_patient_prescription'),
    path('accounts/profile/prescription/visit/<int:visit_id>/' , views.prescription , name = 'prescription'),
    path('accounts/profile/prescription/hitory/<int:doctor_id>/' , views.prescription_history , name = 'prescription_history'),
    path('accounts/profile/prescription/hitory/detail/<int:prescription_id>/' , views.prescription_history_detail , name = 'prescription_history_detail'),
    path('accounts/profile/prescription/hitory/detail/edit/<int:prescription_id>/' , views.prescription_history_detail_edit , name = 'prescription_history_detail_edit'),
    path('accounts/profile/prescription/hitory/detail/delete/<int:prescription_id>/' , views.prescription_history_detail_delete , name = 'prescription_history_detail_delete'),
    #<--- endprescription --->#

    #<--- docotor_detail ---># 
    path('accounts/profile/doctors' , views.show_doctors , name = 'show_doctors'),
    path('accounts/profile/doctors/<int:doctor_id>/' , views.detail_doctor , name = 'detail_doctor'),
    #<--- enddocotor_detail ---># 

    #<--- meds ---># 
    path('accounts/profile/meds' , views.show_meds , name = 'show_meds'),
    path('accounts/profile/meds/<str:med_name>/' , views.detail_meds , name = 'detail_meds'),
    #<--- endmeds ---># 

    #<--- deps ---># 
    path('accounts/profile/departments' , views.deps , name = 'deps'),
    path('accounts/profile/departments/detail/<str:dep_name>/' , views.deps_detail , name = 'deps_detail'),
    #<--- enddeps ---># 
]
