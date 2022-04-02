from django.urls import path
from . import views

urlpatterns = [
    path('about/',views.About, name="about"),
    path('',views.Index,name='index'),
    path('contact', views.contact, name='contact'),
    path('login', views.adminlogin, name='login'),
    path('admin_home', views.admin_home, name='admin_home'),
    path('logout', views.Logout, name='logout'),
    path('doctor',views.doctor,name='doctor'),
    path('add_doctor', views.add_doctor, name='add_doctor'),
    path('view_doctor', views.view_doctor, name='view_doctor'),
    path('delete_doctor/<int:pid>', views.Delete_Doctor, name='delete_doctor'),
    path('add_patient', views.add_patient, name='add_patient'),
    path('view_patient', views.view_patient, name='view_patient'),
    path('delete_patient/<int:pid>', views.Delete_Patient, name='delete_patient'),
    path('add_appointment', views.add_appointment, name='add_appointment'),
    path('view_appointment', views.view_appointment, name='view_appointment'),
    path('delete_appointment/<int:pid>', views.Delete_Appointment, name='delete_appointment'),
    path('edit_doctor/<int:pid>',views.edit_doctor,name='edit_doctor'),
    path('edit_patient/<int:pid>',views.edit_patient,name='edit_patient'),
    path('unread_queries', views.unread_queries, name='unread_queries'),
    path('read_queries', views.read_queries, name='read_queries'),
    path('view_queries/<int:pid>', views.view_queries, name='view_queries'),

]