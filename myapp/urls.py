from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing_page, name='landing_page'),
    path('login/', views.login_page, name='login_page'),
    path('register/', views.register_page, name='register_page'),
    path('profile/', views.profile_page, name='profile_page'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('admindashboard/', views.admindashboard, name='admindashboard'),
    path('userdashboard/', views.userdashboard, name='userdashboard'),
    path('logout/', views.logout_page, name='logout'),
    
    

    path('update-admin-details/', views.update_admin_details, name='update_admin_details'),
    path('update-user-details/', views.update_user_details, name='update_user_details'),
    


]
