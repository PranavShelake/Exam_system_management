from django.contrib import admin
from .models import Exam, Question


# @admin.register(Exam)
# class ExamAdmin(admin.ModelAdmin):
#     list_display = ('exam_type', 'course_name', 'teacher', 'start_time', 'end_time', 'is_active')
#     list_filter = ('exam_type', 'teacher', 'exam_date')
#     actions = ['start_exam', 'close_exam']

#     @admin.action(description='Start selected exams')
#     def start_exam(self, request, queryset):
#         for exam in queryset:
#             exam.start_exam()

#     @admin.action(description='Close selected exams')
#     def close_exam(self, request, queryset):
#         for exam in queryset:
#             exam.close_exam()


# @admin.register(Question)
# class QuestionAdmin(admin.ModelAdmin):
#     list_display = ('exam', 'question_text', 'marks')
