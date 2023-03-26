from django.urls import path
from . import views


urlpatterns = [
    path('login/', views.loginUser, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('signup/', views.signUp, name='signup'),
    path('', views.profiles, name='profiles'),
    path('profile/<str:pk>/', views.userProfile, name='user-profile'),
    path('edit-profile/', views.edit_profile, name='edit-profile'),
    path('add-skill/', views.add_skill, name='add-skill'),
    path('update-skill/<str:pk>/', views.update_skill, name='update-skill'),
    path('delete-skill/<str:pk>/', views.delete_skill, name='delete-skill'),
    path('send-message/<str:pk>/', views.send_message, name='send-message'),
    path('inbox/', views.chat_inbox, name='inbox'),
    path('inbox-detail/<str:pk>/', views.inbox_detail, name='view-message'),
]