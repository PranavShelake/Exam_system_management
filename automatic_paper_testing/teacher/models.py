from django.db import models
from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import User

class Teacher(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="teacher_profile"
    )
    
    enrollment_number = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=255,null=False,blank=False)
    department = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)  # Optional field for teacher bio
    security_key = models.CharField(max_length=255, null=True, blank=True)  # Security key
    is_approved = models.BooleanField(default=False)  # Field for admin approval

    def __str__(self):
        return f"{self.user.email}  ({self.enrollment_number})"


class Exam(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True, blank=True)
    college_name = models.CharField(max_length=255)
    exam_type = models.CharField(max_length=100)
    course_code = models.CharField(max_length=50)
    course_name = models.CharField(max_length=255)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    maximum_marks = models.PositiveIntegerField()
    instructions = models.TextField()
    is_visible = models.BooleanField(default=False)
    exam_date = models.DateField(null=True, blank=True)
    exam_time = models.CharField(max_length=5, blank=True)  # Time as HH:MM format

    def __str__(self):
        return f"{self.exam_type} - {self.course_name} on {self.exam_date.strftime('%d %b %Y') if self.exam_date else 'No Date'}"

class Question(models.Model):
    exam = models.ForeignKey(Exam, related_name="questions", on_delete=models.CASCADE)
    question_text = models.TextField()
    marks = models.PositiveIntegerField()
    correct_answer = models.TextField()

    def __str__(self):
        return self.question_text
