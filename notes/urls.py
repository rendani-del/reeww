from django.urls import path
from . import views

urlpatterns = [
    path('', views.signup_login, name='signup_login'),  # <- this line is essential
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('home/', views.home, name='home'),
    path('your_notes/', views.your_notes, name='your_notes'),
    path('saved_notes/', views.saved_notes, name='saved_notes'),
    path('delete_note/<int:note_id>/', views.delete_note, name='delete_note'),
    path('edit_note/<int:note_id>/', views.edit_note, name='edit_note'),] 
