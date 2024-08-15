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


def patient_history(request , patient_id):
    history = models.Patient.objects.get(id = patient_id)
    return render(request , 'history.html' , {'history' : history})    


def visits(request , patient_id):
    patient = models.Patient.objects.get(id = patient_id)
    visit = models.Visit.objects.filter(patient = patient)
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


def show_patient(request):
    patient = models.Patient.objects.all()
    return render(request , 'patients.html' , {'patient' : patient})

def patient_detail(request , patient_id):
    patient = models.Patient.objects.get(id = patient_id)
    return render(request , 'patient_detail.html' , {'patient' : patient})