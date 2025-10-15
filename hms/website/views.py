from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm
from .models import Record, Patient
from .decorators import group_required
from django.contrib.auth.models import Group

# Create your views here.

def home(request):
    records = None

    if request.user.is_authenticated and request.user.is_staff:
        records = Patient.objects.all()

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # Authenticate
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You have been Logged In!")
            if user.groups.filter(name='patients').exists():
                return redirect('patient')
            else:
                return redirect('home')
        else:
            messages.success(request, "There was An Error Logging In, Please Try Again...")
            return redirect('home')
    else:
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
            role = form.cleaned_data.get('role')
            role = role + 's'
            try:
                group = Group.objects.get(name=role)
            except Group.DoesNotExist:
                messages.error(request, f"The group '{role}' does not exist. Please contact admin.")
                return redirect('register')
            
            user = form.save()
            user.groups.add(group)
            
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "You Have Successfully Registered Welcome !")
            if user.groups.filter(name='patients').exists():
                    return redirect('patient_dashboard')  # your patient dashboard URL name
            else:
                return redirect('home')
    else:
        form = SignUpForm()
        return render(request, 'register.html', {'form': form})
    
    return render(request, 'register.html', {'form': form})

@group_required('patients')
def patient_dashboard(request):
    return render(request, 'patient_dashboard.html', {})

def patient_record(request, pk):
    if request.user.is_authenticated:
        if request.user.is_staff:
            record = Patient.objects.get(id=pk)
            return render(request, 'patient_record.html', {'patient_record': record})
        else:
            messages.success(request, "You Must be Admin to view this Page !")
            return redirect('home')
    else:
        return redirect('home')