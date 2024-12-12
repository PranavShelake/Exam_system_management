from django.urls import path




from .views import remove_student,add_student,student_list,teacher_logout,teacher_verification,teacher_reset_password,teacher_verify_email,teacher_login,teacher_register,exam_delete,toggle_visibility, create_question_paper, teacher_dashboard,manage_exam, toggle_visibility_off

app_name = 'teacher'
urlpatterns = [
    path('exam/<int:exam_id>/toggle_visibility/', toggle_visibility, name='toggle_visibility'),
    path('exam/<int:exam_id>/toggle_visibility_off/', toggle_visibility_off, name='toggle_visibility_off'),
    path('teacher_dashboard/', teacher_dashboard, name='teacher_dashboard'),
    path('manage_exam/', manage_exam, name='manage_exam'),
    path('create_question_paper/', create_question_paper, name='create_question_paper'),
    path('exam/<int:exam_id>/delete/', exam_delete, name='exam_delete'),
    path('student_list/', student_list, name='student_list'),

    path('teacher_login/', teacher_login, name='teacher_login'),
    path('teacher_register/', teacher_register, name='teacher_register'),
    path('teacher_verify_email/', teacher_verify_email, name='teacher_verify_email'),
    path('teacher_reset_password/<int:id>/', teacher_reset_password, name='teacher_reset_password'),
    path('teacher_verification/', teacher_verification, name='teacher_verification'),
    path('teacher_logout/', teacher_logout, name='teacher_logout'),  
     
    path('add-student/<int:student_id>/', add_student, name='add_student'),
    path('remove-student/<int:student_id>/', remove_student, name='remove_student')

]
