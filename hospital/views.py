import email
from operator import countOf
from django.core.mail import send_mail
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,logout,login
from .models import *
from datetime import date
from hospitalmanagement import settings

# Create your views here.

def About(request):
    return render(request,'about.html')

def Index(request):
    return render(request,'index.html')

def doctor(request):
    doc = Doctor.objects.all()
    d = {'doc':doc}
    return render(request,'doctor.html',d)

def contact(request):
    error = ""
    if request.method == 'POST':
        n = request.POST['name']
        c = request.POST['contact']
        e = request.POST['email']
        s = request.POST['subject']
        m = request.POST['message']
        try:
            Contact.objects.create(name=n, contact=c, email=e, subject=s, message=m, msgdate=date.today(), isread="no")
            error = "no"
        except:
            error = "yes"
    return render(request, 'contact.html', locals())


def adminlogin(request):
    error = ""
    if request.method == 'POST':
        u = request.POST['uname']
        p = request.POST['pwd']
        user = authenticate(username=u, password=p)
        try:
            if user.is_authenticated:
                login(request, user)
                error = "no"
            else:
                error = "yes"
        except:
            error = "yes"
    return render(request,'login.html', locals())


def admin_home(request):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    dc = Doctor.objects.all().count()
    pc = Patient.objects.all().count()
    ac = Appointment.objects.all().count()
    uq = len(Contact.objects.filter(isread="no"))
    d = {'dc': dc, 'pc': pc, 'ac': ac,'uq':uq}
    return render(request,'admin_home.html', d)

def Logout(request):
    logout(request)
    return redirect('index')

def add_doctor(request):
    error=""
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method=='POST':
        n = request.POST['name']
        m = request.POST['mobile']
        sp = request.POST['special']
        image=request.FILES['image']

        try:
            Doctor.objects.create(name=n,mob=m,special=sp,image=image)
            error="no"
        except:
            error="yes"
    return render(request,'add_doctor.html', locals())

def view_doctor(request):
    if not request.user.is_authenticated:
        return redirect('login')
    doc = Doctor.objects.all()
    d = {'doc':doc}
    return render(request,'view_doctor.html', d)

def Delete_Doctor(request,pid):
    if not request.user.is_authenticated:
        return redirect('login')
    doctor = Doctor.objects.get(id=pid)
    doctor.delete()
    return redirect('view_doctor')

def edit_doctor(request,pid):
    error = ""
    if not request.user.is_authenticated:
        return redirect('login')
    # user = request.user
    doctor = Doctor.objects.get(id=pid)
    if request.method == "POST":
        n1 = request.POST['name']
        m1 = request.POST['mobile']
        s1 = request.POST['special']
        doctor.name = n1
        doctor.mob = m1
        doctor.special = s1

        try:
            doctor.save()
            error = "no"
        except:
            error = "yes"
    return render(request, 'edit_doctor.html', locals())


def add_patient(request):
    error = ""
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == 'POST':
        n = request.POST['name']
        g = request.POST['gender']
        m = request.POST['mobile']
        a = request.POST['address']
        e = request.POST['email']
        try:
            Patient.objects.create(name=n, gender=g, contact=m, address=a, email=e)
            error = "no"
        except:
            error = "yes"
    return render(request,'add_patient.html', locals())


def view_patient(request):
    if not request.user.is_authenticated:
        return redirect('login')
    pat = Patient.objects.all()
    d = {'pat':pat}
    return render(request,'view_patient.html', d)


def Delete_Patient(request,pid):
    if not request.user.is_authenticated:
        return redirect('login')
    patient = Patient.objects.get(id=pid)
    patient.delete()
    return redirect('view_patient')


def edit_patient(request,pid):
    error = ""
    if not request.user.is_authenticated:
        return redirect('login')
    user = request.user
    patient = Patient.objects.get(id=pid)
    if request.method == "POST":
        n1 = request.POST['name']
        m1 = request.POST['mobile']
        g1 = request.POST['gender']
        a1 = request.POST['address']
        e1 = request.POST['email']

        patient.name = n1
        patient.contact= m1
        patient.gender = g1
        patient.address = a1
        patient.email = e1
        try:
            patient.save()
            error = "no"
        except:
            error = "yes"
    return render(request, 'edit_patient.html', locals())


def add_appointment(request):
    error=""
    if not request.user.is_authenticated:
        return redirect('login')
    doctor1 = Doctor.objects.all()
    patient1 = Patient.objects.all()
    if request.method=='POST':
        d = request.POST['doctor']
        p = request.POST['patient']
        d1 = request.POST['date']
        t = request.POST['time']
        em = request.POST['email']

        doctor = Doctor.objects.filter(name=d).first()
        patient = Patient.objects.filter(name=p).first()
        try:
            subject="Appointment"
            message="Dear"+" "+p+" "+"your appointment is confirmed for"+" "+d+" "+"on"+" "+d1+" "+"at"+" "+t
            reciptent=request.POST['email']
            send_mail(subject,message,settings.EMAIL_HOST_USER,[reciptent],fail_silently=False)
            messages.success(request,'Mail send successfully')

            Appointment.objects.create(doctor=doctor, patient=patient, date1=d1, time1=t, email1=em)
            error="no"
            return redirect('view_appointment')
        except:
            error="yes" 
    d = {'doctor':doctor1,'patient':patient1,'error':error}
    return render(request,'add_appointment.html', d)


def view_appointment(request):
    if not request.user.is_authenticated:
        return redirect('login')
    appointment = Appointment.objects.all()
    d = {'appointment':appointment}
    return render(request,'view_appointment.html', d)

def Delete_Appointment(request,pid):
    if not request.user.is_authenticated:
        return redirect('login')
    appointment1 = Appointment.objects.get(id=pid)
    appointment1.delete()
    return redirect('view_appointment')

def unread_queries(request):
    if not request.user.is_authenticated:
        return redirect('login')
    contact = Contact.objects.filter(isread="no")
    return render(request,'unread_queries.html',locals())


def read_queries(request):
    if not request.user.is_authenticated:
        return redirect('login')
    contact = Contact.objects.filter(isread="yes")
    contact.isread = "yes"
    return render(request,'read_queries.html', locals())


def view_queries(request,pid):
    if not request.user.is_authenticated:
        return redirect('login')
    contact = Contact.objects.get(id=pid)
    contact.isread = "yes"
    contact.save()
    return render(request,'view_queries.html', locals())

