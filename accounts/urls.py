from django.urls import path
from . import views


app_name = 'accounts'
urlpatterns = [
    path('login/', views.login_page, name='login_page'),
    path('logout/', views.logout_page, name='logout_page'),
    path('register/', views.register_page, name='register_page'),
    path('dashboard/', views.dashboard_page, name='dashboard_page'),
    path('dashboard/edit_profile/', views.edit_profile_page, name='edit_profile_page'),
    path('dashboard/show_orders/', views.show_orders, name='show_orders'),
]
