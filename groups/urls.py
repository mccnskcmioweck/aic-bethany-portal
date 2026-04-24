from django.urls import path
from . import views
urlpatterns = [
    path('', views.group_list, name='group_list'),
    path('my-groups/', views.my_groups, name='my_groups'),
    path('<int:pk>/', views.group_detail, name='group_detail'),
    path('<int:pk>/join/', views.join_group, name='join_group'),
    path('<int:pk>/leave/', views.leave_group, name='leave_group'),
]
