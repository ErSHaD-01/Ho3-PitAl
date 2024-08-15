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
    
    path('accounts/profile/history/<int:patient_id>' , views.patient_history , name = 'patient_history'),
    
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

]
