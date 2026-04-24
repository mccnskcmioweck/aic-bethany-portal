from django.urls import path
from . import views
urlpatterns = [
    path('', views.report_dashboard, name='report_dashboard'),
    path('attendance/', views.attendance_list, name='attendance_list'),
    path('attendance/new/', views.attendance_create, name='attendance_create'),
    path('attendance/<int:pk>/', views.attendance_detail, name='attendance_detail'),
    path('sunday-school/', views.sunday_school_list, name='sunday_school_list'),
    path('sunday-school/new/', views.sunday_school_create, name='sunday_school_create'),
    path('sunday-school/<int:pk>/', views.sunday_school_detail, name='sunday_school_detail'),
    path('offerings/', views.offering_list, name='offering_list'),
    path('offerings/new/', views.offering_create, name='offering_create'),
    path('offerings/<int:pk>/', views.offering_detail, name='offering_detail'),
    path('programs/', views.program_list, name='program_list'),
    path('programs/new/', views.program_create, name='program_create'),
    path('programs/<int:pk>/', views.program_detail, name='program_detail'),
]
