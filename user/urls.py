from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.LoginPage, name='login'),
    path('logout/', views.LogoutPage, name='logout'), 
    path('signup/', views.SignupPage, name='signup'), 
    path('venues/', views.conference_hall_details, name='venues'),
    path('payment/<int:conference_id>/', views.PaymentView.as_view(), name='payment'),
    path('profile/', views.profile, name='profile'),
    path('contact/', views.contact, name='contact'),
    
]
