from django.urls import path
from . import views
#from .views import UserRegistrationView, UserLoginView, UserLogoutView


urlpatterns = [
    path('', views.apiOverview, name="api-overview"),
    path('note-list/', views.noteList, name="note-list"),
    path('note-view/<str:pk>/', views.noteView, name="note-view"),
    path('note-add/', views.noteAdd, name="note-add"),
    path('note-update/<str:pk>/', views.noteUpdate, name='note-update'),
    path('note-delete/<str:pk>/', views.noteDelete, name='note-delete'),
    #path('register/', views.register_user, name='user-registration'),
    path('register/', views.UserRegistrationView.as_view(), name='user-registration'),
    path('login/', views.UserLoginView.as_view(), name='user-login'),
    path('logout/', views.UserLogoutView.as_view(), name='user-logout'),
    path('change_password/', views.ChangePasswordView.as_view(), name='change-password'),
]