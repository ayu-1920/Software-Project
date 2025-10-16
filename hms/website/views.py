from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, AddPatientForm
from .models import Record, Patient
from .decorators import *
from django.contrib.auth.models import Group

# Create your views here.

def handle_user_login(request, username, password):
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        messages.success(request, "You have been Logged In!")
        group_names = ['patients', 'doctors']
        for gn in group_names:
            if user.groups.filter(name=gn).exists():
                # To return patients as patient
                return redirect(f'{gn[:-1]}')
        return redirect('home')
    else:
        messages.error(request, "There was an error logging in. Please try again.")
        return redirect('home')

def home(request):
    records = None

    if request.user.is_authenticated and request.user.is_staff:
        records = Patient.objects.all()

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        return handle_user_login(request, username, password)

    return render(request, 'home.html', {'records': records})

def login_user(request):
    pass

def logout_user(request):
    logout(request)
    messages.success(request, "You Have Been Logged Out...")
    return redirect('home')



def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            # Authenticate and Login
            role = f"{form.cleaned_data.get('role')}s"
            try:
                group = Group.objects.get(name=role)
            except Group.DoesNotExist:
                messages.error(request, f"The group '{role}' does not exist. Please contact admin.")
                return redirect('register')
            
            user = form.save()
            user.groups.add(group)            
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            return handle_user_login(request, username, password)

    form = SignUpForm()
    return render(request, 'register.html', {'form': form})

@login_required
@group_required('patients')
def patient_dashboard(request):
    return render(request, 'patient/patient_dashboard.html', {})

@login_required
@group_required('doctors')
def doctor_dashboard(request):
    return render(request, 'doctor/doctor_dashboard.html', {})


@login_required
@staff_required
def patient_record(request, pk):
    try:
        record = Patient.objects.get(id=pk)
        return render(request, 'patient_record.html', {'patient_record': record})
    except Patient.DoesNotExist:
        messages.error(request, "Patient record not found.")
        return redirect('home')
    
@login_required
@staff_required    
def delete_record(request, pk):
    try:
        delete_it = Patient.objects.get(id=pk)
        delete_it.delete()
        messages.success(request, "Records Deleted Successfully ... ")
        return redirect('home')
    except Patient.DoesNotExist:
        messages.error(request, "Patient record not found.")
        return redirect('home')

@login_required
@staff_required
def add_record(request):
    form = AddPatientForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            add_record = form.save()
            messages.success(request, "Patient Added ... ")
            return redirect('home')
    
    return render(request, 'add_record.html', {'form': form})
        
    
    
@login_required
@staff_required
def update_record(request, pk):
    try:
        curr = Patient.objects.get(id=pk)
        form = AddPatientForm(request.POST or None, instance=curr)
        if request.method == "POST" and form.is_valid():
            form.save()
            messages.success(request, "Record Has Been Updated ! ")
            return redirect('home')
        return render(request, 'update_record.html', {'form': form})
    except Patient.DoesNotExist:
        messages.error(request, "Patient record not found.")
        return redirect('home')