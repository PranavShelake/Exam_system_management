from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, logout, login as auth_login
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from .models import Exam, Teacher
from student.models import Student
from automatic_paper_testing.email import sent_mail
import random

# Add Student
@login_required(login_url='/teacher_login/')
def add_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    teacher = request.user.teacher_profile  # Assuming Teacher model is linked to User
    teacher.students.add(student)
    messages.success(request, 'Student added successfully.')
    return redirect('teacher:student_list')

# Remove Student
@login_required(login_url='/teacher_login/')
def remove_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    teacher = request.user.teacher_profile
    teacher.students.remove(student)
    messages.success(request, 'Student removed successfully.')
    return redirect('teacher:student_list')

# Dashboard
@login_required(login_url='/teacher_login/')
def teacher_dashboard(request):
    return render(request, 'teacher_dashboard.html')

# Create Question Paper
@login_required
def create_question_paper(request):
    if request.method == 'POST':
        college_name = request.POST.get("college_name")
        exam_type = request.POST.get("exam_type")
        course_code = request.POST.get("course_code")
        course_name = request.POST.get("course_name")
        exam_date = request.POST.get("exam_date")
        exam_time = request.POST.get("exam_time")
        maximum_marks = request.POST.get("maximum_marks")
        instructions = request.POST.get("instructions")

        teacher_instance = request.user.teacher_profile

        try:
            exam = Exam.objects.create(
                teacher=teacher_instance,
                college_name=college_name,
                exam_type=exam_type,
                course_code=course_code,
                course_name=course_name,
                exam_date=exam_date,
                exam_time=exam_time,
                maximum_marks=maximum_marks,
                instructions=instructions
            )
            messages.success(request, "Question paper created successfully.")
            return redirect('teacher:manage_exam')
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
            return redirect('teacher:create_question_paper')

    return render(request, "create_paper.html")

# Manage Exam
@login_required(login_url='/teacher_login/')
def manage_exam(request):
    exams = Exam.objects.filter(teacher=request.user.teacher_profile)
    if request.method == 'POST':
        exam_id = request.POST.get('exam_id')
        if exam_id:
            exam = get_object_or_404(Exam, id=exam_id)
            exam.delete()
            messages.success(request, 'Exam deleted successfully.')
            return redirect('teacher:manage_exam')
    return render(request, 'manage_exam.html', {'exams': exams})

# Toggle Visibility
@login_required(login_url='/teacher_login/')
def toggle_visibility(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id, teacher=request.user.teacher_profile)
    exam.is_visible = True
    exam.save()
    messages.success(request, "Exam visibility has been turned on.")
    return redirect('teacher:manage_exam')

@login_required(login_url='/teacher_login/')
def toggle_visibility_off(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id, teacher=request.user.teacher_profile)
    exam.is_visible = False
    exam.save()
    messages.success(request, "Exam visibility has been turned off.")
    return redirect('teacher:manage_exam')

# Delete Exam
@login_required(login_url='/teacher_login/')
def exam_delete(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id, teacher=request.user.teacher_profile)
    exam.delete()
    messages.success(request, "Exam has been successfully deleted.")
    return redirect('teacher:manage_exam')

# Student List
@login_required(login_url='/teacher_login/')
def student_list(request):
    query = request.GET.get('q')
    students = Student.objects.all()
    if query:
        students = students.filter(enrollment_number__icontains=query)
    return render(request, 'student_list.html', {'students': students, 'query': query})

# Teacher Login
def teacher_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not email or not password:
            messages.error(request, 'All fields are required.')
            return redirect('teacher:teacher_login')

        try:
            teacher_user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, 'Invalid Email or Password.')
            return redirect('teacher:teacher_login')

        if hasattr(teacher_user, 'teacher_profile'):
            user = authenticate(request, username=teacher_user.username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('teacher:teacher_dashboard')
            else:
                messages.error(request, 'Invalid Email or Password.')
        else:
            messages.error(request, 'No teacher account associated with this email.')

        return redirect('teacher:teacher_login')
    return render(request, 'teacher_login.html')

# Teacher Registration
def teacher_register(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        first_name = request.POST.get('fname')
        password = request.POST.get('password')
        security_key = request.POST.get('key')

        if not email or not first_name or not password or not security_key:
            messages.error(request, 'All fields are required.')
            return redirect('teacher:teacher_register')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email is already taken.')
            return redirect('teacher:teacher_register')

        try:
            validate_password(password)
            gen_otp = random.randint(1000, 9999)
            sent_mail(first_name, email, gen_otp)

            hashed_password = make_password(password)
            request.session.update({
                'first_name': first_name,
                'email': email,
                'hashed_password': hashed_password,
                'security_key': security_key,
                'gen_otp': gen_otp,
            })

            messages.success(request, 'OTP sent to your email.')
            return redirect('teacher:teacher_verify_email')

        except ValidationError as e:
            messages.error(request, str(e))
        except Exception as e:
            messages.error(request, f'Error occurred during registration: {e}')

        return redirect('teacher:teacher_register')
    return render(request, 'teacher_register.html')

# Teacher Verification
def teacher_verify_email(request):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        gen_otp = request.session.get('gen_otp')

        if otp == str(gen_otp):
            first_name = request.session.get('first_name')
            email = request.session.get('email')
            hashed_password = request.session.get('hashed_password')
            security_key = request.session.get('security_key')

            request.session.flush()
            user = User.objects.create_user(username=email, email=email, first_name=first_name)
            user.set_password(hashed_password)
            user.save()
            Teacher.objects.create(user=user, security_key=security_key)

            messages.success(request, 'Teacher registration successful. Please login.')
            return redirect('teacher:teacher_login')

        messages.error(request, 'OTP is incorrect.')
        return redirect('teacher:teacher_verify_email')

    return render(request, 'teacher_verify_email.html')

# Teacher Password Reset
def teacher_reset_password(request, id):
    if request.method == 'POST':
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if password == password2:
            try:
                validate_password(password)
                user = User.objects.get(id=id)
                user.set_password(password)
                user.save()
                messages.success(request, 'Password reset successfully.')
                return redirect('teacher:teacher_login')
            except ValidationError as e:
                messages.error(request, str(e))
            except User.DoesNotExist:
                messages.error(request, 'User does not exist.')

        else:
            messages.error(request, 'Passwords do not match.')
        return redirect('teacher:teacher_reset_password', id=id)

    return render(request, 'teacher_reset_password.html')

# Teacher Verification
def teacher_verification(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        security_key = request.POST.get('key')

        if not email or not security_key:
            messages.error(request, 'All fields are required.')
            return redirect('teacher:teacher_verification')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, 'Invalid email.')
            return redirect('teacher:teacher_verification')

        try:
            teacher_account = Teacher.objects.get(user=user)
            if teacher_account.security_key == security_key:
                return redirect('teacher:teacher_reset_password', id=user.id)
            messages.error(request, 'Invalid security key.')

        except Teacher.DoesNotExist:
            messages.error(request, 'Account does not exist for this teacher.')

        return redirect('teacher:teacher_verification')
    return render(request, 'teacher_verification.html')

# Logout
def teacher_logout(request):
    logout(request)
    messages.success(request, 'Logged out successfully.')
    return redirect('ems:ems')
