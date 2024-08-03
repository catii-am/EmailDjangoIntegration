from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('emails/<int:email_account_id>/', views.email_list, name='email_list'),
]
