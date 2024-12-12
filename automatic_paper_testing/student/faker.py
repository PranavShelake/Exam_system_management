import random
from faker import Faker

from django.contrib.auth.models import User
from student.models import Student

# Initialize Faker for Indian locale
fake = Faker('en_IN')

used_enrollment_numbers = set()

def generate_unique_enrollment_number():
    while True:
        enrollment_number = random.randint(100000, 999999)
        if enrollment_number not in used_enrollment_numbers:
            used_enrollment_numbers.add(enrollment_number)
            return enrollment_number

def create_students(count):
    for _ in range(count):
        # Generate Indian-specific name and email
        first_name = fake.first_name()
        last_name = fake.last_name()
        full_name = f"{first_name} {last_name}"
        email = f"{first_name.lower()}{last_name.lower()}{random.randint(1, 99)}@gmail.com"

        # Create User
        username = email.split("@")[0]
        user = User.objects.create_user(
            username=username, email=email
        )
        user.set_password('123')  # Store the password as a hash
        user.save() 
        # Create Student
        student = Student.objects.create(
            user=user,
            name=full_name,  # Generates Indian-style full names
            enrollment_number=generate_unique_enrollment_number(),
            course=random.choice(["CSE", "ENTC", "ECE", "DS", "IT"]),  # Indian engineering branches
            phone_number=f"+91-{random.randint(6000000000, 9999999999)}",  # Indian phone number format
            security_key="student",
            is_approved=False,
        )

        print(f"Created student: {student}")
