from django.db import models
from django.contrib.auth.models import User

from django.db import models
from django.contrib.auth.models import User

class Student(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="student_profile"
    )
    teachers = models.ManyToManyField(
        'teacher.Teacher',  # Referencing the Teacher model in the teacher app
        related_name="students",
        blank=True
    )
    name = models.CharField(max_length=255,null=False,blank=False)
    enrollment_number = models.CharField(max_length=100, unique=True)
    course = models.CharField(max_length=255)  # Course name or code
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    security_key = models.CharField(max_length=255, null=True, blank=True)  # Security key
    is_approved = models.BooleanField(default=False)  # Field for admin approval

    def __str__(self):
        return f"{self.user.email} ({self.enrollment_number})"
