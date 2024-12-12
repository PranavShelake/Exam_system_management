from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth import authenticate, logout, login as auth_login
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from student.models import Student
import random
from automatic_paper_testing.email import sent_mail

@login_required(login_url='/student_login/')
def student_dashboard(request):
    return render(request, 'student_dashboard.html')

def student_exam(request):
    return render(request, 'student_exam.html')

def student_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not email or not password:
            messages.error(request, 'All fields are required.')
            return redirect('student:student_login')

        try:
            student_user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, 'Invalid Email or Password.')
            return redirect('student:student_login')

        user = authenticate(request, username=student_user.username, password=password)
        if user is not None:
            if hasattr(student_user, 'student_profile'):
                auth_login(request, user)
                return redirect('student:student_dashboard')
            else:
                messages.error(request, 'No student account associated with this email.')
        else:
            messages.error(request, 'Invalid Email or Password.')

        return redirect('student:student_login')
    return render(request, 'student_login.html')

def student_verify_email(request):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        gen_otp = request.session.get('gen_otp')

        if otp == str(gen_otp):
            name = request.session.get('name')
            email = request.session.get('email')
            hashed_password = request.session.get('hashed_password')
            security_key = request.session.get('security_key')
            phone_number = request.session.get('phone_number')
            course = request.session.get('course')
            enrollment_number = request.session.get('enrollment_number')

            request.session.flush()

            user = User.objects.create_user(username=email, email=email, first_name=name)
            user.password = hashed_password
            user.save()

            Student.objects.create(
                user=user,
                security_key=security_key,
                name=name,
                phone_number=phone_number,
                course=course,
                enrollment_number=enrollment_number
            )

            messages.success(request, 'Student registration successful. Please login.')
            return redirect('student:student_login')
        else:
            messages.error(request, 'OTP is incorrect.')
            return redirect('student:student_verify_email')

    return render(request, 'student_verify_email.html')

def student_register(request):
    if request.method == 'POST':
        data = request.POST
        email = data.get('email')
        name = data.get('name')
        password = data.get('password')
        security_key = data.get('key')
        course = data.get('course')
        phone_number = data.get('phone_number')
        enrollment_number = data.get('enrollment_number')

        if not email or not name or not password or not security_key or not enrollment_number:
            messages.error(request, 'All fields are required.')
            return redirect('student:student_register')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email is already taken.')
            return redirect('student:student_register')

        if Student.objects.filter(enrollment_number=enrollment_number).exists():
            messages.error(request, 'Enrollment number is already taken.')
            return redirect('student:student_register')

        try:
            gen_otp = random.randint(1000, 9999)
            sent_mail(name, email, gen_otp)

            hashed_password = make_password(password)
            request.session['name'] = name
            request.session['email'] = email
            request.session['hashed_password'] = hashed_password
            request.session['enrollment_number'] = enrollment_number
            request.session['security_key'] = security_key
            request.session['course'] = course
            request.session['phone_number'] = phone_number
            request.session['gen_otp'] = gen_otp

            messages.success(request, 'OTP sent to your email.')
            return redirect('student:student_verify_email')

        except Exception as e:
            messages.error(request, f'Error occurred during registration: {e}')
            return redirect('student:student_register')

    return render(request, 'student_register.html')

def student_reset_password(request, id):
    if request.method == 'POST':
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if password == password2:
            try:
                user = User.objects.get(id=id)
                user.set_password(password)
                user.save()
                messages.success(request, 'Password reset successfully.')
                return redirect('student:student_login')
            except User.DoesNotExist:
                messages.error(request, 'User does not exist.')
                return redirect('student:student_login')
        else:
            messages.error(request, 'Passwords do not match.')
            return redirect('student:student_reset_password', id=id)

    return render(request, 'student_reset_password.html')

def student_verification(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        security_key = request.POST.get('key')

        if not email or not security_key:
            messages.error(request, 'All fields are required.')
            return redirect('student:student_verification')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, 'Invalid email.')
            return redirect('student:student_verification')

        try:
            student_account = Student.objects.get(user=user)
            if student_account.security_key == security_key:
                return redirect('student:student_reset_password', id=user.id)
            else:
                messages.error(request, 'Invalid security key.')
                return redirect('student:student_verification')
        except Student.DoesNotExist:
            messages.error(request, 'Account does not exist for this student.')
            return redirect('student:student_verification')

    return render(request, 'student_verification.html')

def student_logout(request):
    logout(request)
    messages.success(request, 'Logged out successfully.')
    return redirect('ems:ems')
