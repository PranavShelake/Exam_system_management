from django.urls import path
from .views import student_dashboard,student_exam,student_login,student_register,student_verify_email,student_verification,student_reset_password,student_logout
app_name = 'student'
urlpatterns = [
    path('student_dashboard/', student_dashboard, name='student_dashboard'),
    path('student_exam/', student_exam, name='student_exam'),



    path('student_login/', student_login, name='student_login'),
    path('student_register/', student_register, name='student_register'),
    path('student_verify_email/', student_verify_email, name='student_verify_email'),
    path('student_reset_password/<int:id>/', student_reset_password, name='student_reset_password'),
    path('student_verification/', student_verification, name='student_verification'),
    path('student_logout/', student_logout, name='student_logout'),  
]
