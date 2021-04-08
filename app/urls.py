from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('form/', views.form_data, name='form'),
    path('update/<int:pk>/', views.update, name='update'),
    path('delete/<int:pk>/', views.delete, name='deleteStd'),

    path('followup_form/', views.follow_up_form, name='followup'),
    path('followup_all/', views.follow_up_all, name='followupall'),

    path('followup_detail/<int:pk>/', views.follow_up_detail, name='followupdetail'),
    path('followup_delete/<int:pk>/', views.follow_up_delete, name='followupdelete'),

    path('login/', views.login_form, name='login'),
    path('logout/', views.logout_user, name='logout'),
]
