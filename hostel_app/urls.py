from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('dashboard/', views.student_dashboard, name='dashboard'),
    path('rooms/', views.room_list, name='room_list'),
    path('room/<int:room_id>/apply/', views.apply_room, name='apply_room'),
    path('my-room/', views.my_room, name='my_room'),
    path('complaints/', views.complaints_list, name='complaints'),
    path('complaints/new/', views.submit_complaint, name='submit_complaint'),
    
    # Admin Panel
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('manage-rooms/', views.manage_rooms, name='manage_rooms'),
    path('manage-rooms/add/', views.add_room, name='add_room'),
    path('manage-rooms/edit/<int:room_id>/', views.edit_room, name='edit_room'),
    path('manage-rooms/delete/<int:room_id>/', views.delete_room, name='delete_room'),
    path('manage-students/', views.manage_students, name='manage_students'),
    path('manage-allocations/', views.manage_allocations, name='manage_allocations'),
    path('manage-allocations/<int:allocation_id>/<str:action>/', views.approve_reject_allocation, name='approve_reject_allocation'),
    path('manage-complaints/', views.manage_complaints, name='manage_complaints'),
    path('manage-complaints/<int:complaint_id>/resolve/', views.resolve_complaint, name='resolve_complaint'),
]
