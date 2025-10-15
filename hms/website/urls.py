from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('patient/', views.patient_dashboard, name='patient'),
    path('patient_record/<int:pk>', views.patient_record, name='patient_record'),
]