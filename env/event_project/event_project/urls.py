"""
URL configuration for event_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from DreamScape import views


# Add logs to the views
urlpatterns = [
    path('dj-admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('events/', views.events, name='events'),
    path('booking/',views.booking,name='booking'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('engagement/',views.engagement, name='engagement'),
    path('wedding/',views.wedding, name='wedding'),
    path('reception/',views.reception, name='reception'),
    path('birthday/',views.birthday, name='birthday'),
    path('bachelor/',views.bachelor, name='bachelor'),
    path('bride/',views.bride, name='bride'),
    path('search/', views.search, name='search'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('adminlogin/', views.adminlogin, name="adminlogin"),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('userevent/',views.User_event,name="userevent"),
    path('signup1/',views.signup1,name='signup1'),
    path('other_events/',views.other_events,name='other_events'),
    path('payment/<int:event_id>/', views.payment_page, name='payment'),
    path('deleteevent/<str:name>/<str:eventname>', views.deleteevent, name="deleteevent"),
    path('updateevent/<str:name>/<str:eventname>', views.updateevent, name="updateevent"),
    path('updateeventdetails/', views.updateeventdetails, name="updateeventdetails"),
    path('payment/<int:event_id>/', views.payment_page, name='payment'),
    path('payment/methods/<int:event_id>/', views.choose_payment, name='choose_payment'),
    path('pay/upi/<int:event_id>/', views.pay_upi, name='pay_upi'),
    path('pay/card/<int:event_id>/', views.pay_card, name='pay_card'),
    path('pay/netbanking/<int:event_id>/', views.pay_netbanking, name='pay_netbanking'),
    path('pay/paytm/<int:event_id>/', views.pay_paytm, name='pay_paytm'),
    path('payment/success/', views.payment_success, name='payment_success'),
    path('pay/<int:event_id>/', views.pay_now, name='pay_now'), 
]

