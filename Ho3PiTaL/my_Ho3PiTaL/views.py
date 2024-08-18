from django.shortcuts import render , redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate , login as Login , logout as Logout , update_session_auth_hash
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError

from . import forms
from . import models
# Create your views here.

def home(request):
    return render(request , 'home.html')

#<--- register/login/profile --->#
def register_patient(request):
    if request.method == 'POST':
        form = forms.PatientRegistrationForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = models.User.objects.create_user(
                username = cd['username'],
                password = cd['password'],
                first_name = cd['first_name'],
                last_name = cd['last_name']
            )
            patient = form.save(commit = False)
            patient.user = user
            patient.save()
            return redirect('home')
    else:
        form = forms.PatientRegistrationForm()
    return render(request, 'register.html', {'form': form})

def login(request):
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(
                request,
                username = cd['username'],
                password = cd['password']
            )
            if user is not None:
                Login(request , user)
                return redirect('profile')
            else:
                return HttpResponse('not ok') 
    else:
        form = forms.LoginForm()
    return render(request , 'login.html' , {'form' : form}) 

def logout(request):
    Logout(request)
    return HttpResponse('you loged out')

@login_required
def profile(request):
    user = request.user
    user_data = None
    who_is_user = None
    try:
        user_data = models.Patient.objects.get(user = user)
        who_is_user = 'Patient'
    except models.Patient.DoesNotExist:
        pass

    if who_is_user is None:
        try:
            user_data = models.Doctor.objects.get(user = user)
            who_is_user = 'Doctor'
        except models.Doctor.DoesNotExist:
            pass

    if who_is_user is None:
        try:
            user_data = models.Staff.objects.get(user = user)
            who_is_user = 'Staff'
        except models.Staff.DoesNotExist:
            pass

    return render(request, 'profile.html', {'who_is_user' : who_is_user , 'user_data': user_data})

def edit_profile(request):
    user = request.user
    if request.method == 'POST':
        form = forms.EditProfileForm(request.POST , instance = user)
        if form.is_valid():
            if form.cleaned_data['password']:
                user.set_password(form.cleaned_data['password'])
            form.save()
            update_session_auth_hash(request, user)
            return redirect('profile')
    else:
        form = forms.EditProfileForm(instance = user)

    return render(request, 'edit_profile.html', {'form': form})
#<--- endregister/login/profile --->#

#<--- history --->#
def history(request , patient_id):
    patient = models.Patient.objects.get(id = patient_id)
    return render(request , 'what_history.html' , {'patient' : patient})

def disease_history(request , patient_id):
    patient = models.Patient.objects.get(id = patient_id)
    disease = models.Prescription.objects.filter(patient = patient)
    return render(request , 'history.html' , {'disease' : disease})    

def visit_history(request , patient_id):
    patient = models.Patient.objects.get(id = patient_id)
    visit = models.Prescription.objects.filter(patient = patient)
    return render(request , 'visit_history.html' , {'visit' : visit})    
#<--- endhistory --->#


#<--- visit --->#
def visits(request , patient_id):
    patient = models.Patient.objects.get(id = patient_id)
    visit = models.Visit.objects.filter(patient = patient , is_confirmed = False)
    return render(request , 'show_visites.html' , {'visit' : visit , 'patient' : patient})

def visit_data(request , visit_id):
    visit = models.Visit.objects.get(id = visit_id)
    return render(request , 'visit_data.html' , {'visit_data' : visit})

def visit_delete(request , visit_id):
    models.Visit.objects.get(id = visit_id).delete()
    if request.user.is_authenticated:
        return redirect('profile')
    else:
        login(request, request.user)
        return redirect('profile')
    
def create_visit(request , patient_id):
    patient = models.Patient.objects.get(id = patient_id)
    if request.method == 'POST':
        form = forms.VisitForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            models.Visit.objects.create(
                doctor = cd['doctor'],
                date = cd['date'],
                text = cd['text'],
                patient = patient,
            )
            if request.user.is_authenticated:
                return redirect('profile')
            else:
                login(request, request.user)
                return redirect('profile')
    else:
        form = forms.VisitForm()
    return render(request , 'visit.html' , {'form' : form})
#<--- endvisit --->#

#<--- patient_detail --->#
def show_patient(request):
    patient = models.Patient.objects.all()
    return render(request , 'patients.html' , {'patient' : patient})

def patient_detail(request , patient_id):
    patient = models.Patient.objects.get(id = patient_id)
    return render(request , 'patient_detail.html' , {'patient' : patient})
#<--- endpatient_detail --->#

#<--- accept_visit --->#
def doctor_visit(request , doctor_id):
    doc = models.Doctor.objects.get(id = doctor_id)
    doctor = models.Visit.objects.filter(doctor = doc , is_confirmed = False)
    return render(request , 'doctor_visist.html' , {'doctor' : doctor})

def doctor_visit_data(request , visit_id):
    visit = models.Visit.objects.get(id = visit_id)
    if request.method == 'POST':
        form = forms.AcceptVisitForm(request.POST , instance = visit)
        if form.is_valid():
            form.save()
            if request.user.is_authenticated:
                return redirect('profile')
            else:
                login(request, request.user)
                return redirect('profile')
    else:
        form = forms.AcceptVisitForm(instance = visit)
    return render(request , 'accept_visit.html' , {'form' : form , 'visit' : visit})   
#<--- endaccept_visit --->#

#<--- prescription ---># 
def show_patient_prescription(request , doctor_id):
    doc = models.Doctor.objects.get(id = doctor_id)
    patient = models.Visit.objects.filter(doctor = doc , prescription_written = False , is_confirmed = True)
    return render(request , 'show_patient_prescription.html' , {'patients' : patient , 'doctor' : doc})

def prescription(request , visit_id):
    visit = models.Visit.objects.get(id = visit_id)
    if request.method == 'POST':
        form = forms.PrescriptionForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            prescription_ = models.Prescription.objects.create(
                doctor = visit.doctor,
                patient = visit.patient,
                department = cd['department'],
                disease = cd['disease'],
                text = cd['text'],
                how_to_use = cd['how_to_use'],
                date = cd['date'],
            )
            prescription_.meds.set(cd['meds'])
            visit.prescription_written = True
            visit.save()
            return redirect('show_patient_prescription' , visit.doctor.id)
            
    else:
        form = forms.PrescriptionForm()
    return render(request , 'prescription.html' , {'form' : form})

def prescription_history(request , doctor_id):
    doc = models.Doctor.objects.get(id = doctor_id)
    prescription = models.Prescription.objects.filter(doctor = doc)
    return render(request , 'prescription_history.html' , {'prescription' : prescription , 'doctor' : doc})

def prescription_history_detail(request , prescription_id):
    prescription = models.Prescription.objects.get(id = prescription_id)
    return render(request , 'prescription_detail.html' , {'prescription' : prescription})

def prescription_history_detail_edit(request , prescription_id):
    prescription = models.Prescription.objects.get(id = prescription_id)
    if request.method == 'POST':
        form = forms.PrescriptionForm(request.POST , instance = prescription)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else :
        form = forms.PrescriptionForm(instance = prescription)
    return render(request , 'prescription_edit.html' , {'form' : form})
 
def prescription_history_detail_delete(request , prescription_id):
    prescription = models.Prescription.objects.get(id = prescription_id).delete()
    return redirect('profile')

def show_prescription(request):
    prescription = models.Prescription.objects.all()
    return render(request , 'prescriptions.html' , {'prescription' : prescription})

def prescription_detail(request , prescription_id):
    prescription = models.Prescription.objects.get(id = prescription_id)
    return render(request , 'prescriptions_detail.html' , {'prescription' : prescription})
#<--- endprescription ---># 

#<--- docotor_detail ---># 
def show_doctors(request):
    doctor = models.Doctor.objects.all()
    return render(request , 'doctors.html' , {'doctor' : doctor})

def detail_doctor(request , doctor_id):
    doctor = models.Doctor.objects.get(id = doctor_id)
    return render(request , 'doctor_detail.html' , {'doctor' : doctor})
#<--- enddocotor_detail ---># 

#<--- meds ---># 
def show_meds(request):
    meds = models.Medication.objects.all()
    return render(request , 'meds.html' , {'meds' : meds})

def detail_meds(request , med_name):
    meds = models.Medication.objects.get(name = med_name)
    return render(request , 'meds_detail.html' , {'meds' : meds})
#<--- endmeds ---># 

#<--- deps ---># 
def deps(request):
    dep = models.Department.objects.all()
    return render(request , 'deps.html' , {'dep' : dep})

def deps_detail(request , dep_name):
    dep = models.Department.objects.get(name = dep_name)
    return render(request , 'deps_detail.html' , {'dep' : dep})
#<--- enddeps ---># 
