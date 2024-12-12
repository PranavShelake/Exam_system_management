import random
from faker import Faker

from django.contrib.auth.models import User
from teacher.models import Teacher

# Initialize Faker for English locale
fake = Faker('en_IN')  # English names, Indian locale

used_teacher_usernames = set()
used_enrollment_numbers = set()
def generate_unique_enrollment_number():
    while True:
        enrollment_number = random.randint(100000, 999999)
        if enrollment_number not in used_enrollment_numbers:
            used_enrollment_numbers.add(enrollment_number)
            return enrollment_number


def generate_unique_teacher_username(full_name):
    while True:
        username = f"{full_name}{random.randint(1000, 9999)}"
        if username not in used_teacher_usernames:
            used_teacher_usernames.add(username)
            return username

def create_teachers(count):
    for _ in range(count):
        # Generate English name and email for the teacher
        
        enrollment_number=generate_unique_enrollment_number(),
        first_name = fake.first_name()
        last_name = fake.last_name()
        full_name = f"{first_name} {last_name}"
        email = f"{first_name.lower()}{last_name.lower()}{random.randint(1, 999)}@gmail.com"

        # Create User for the teacher
        username = generate_unique_teacher_username(full_name)  # Ensures unique usernames for teachers
        user = User.objects.create_user(
            username=username, email=email  # Default password
        )
        
        user.set_password('123')  # Store the password as a hash
        user.save() 
        # Generate a random department
        department = random.choice(["CSE", "ECE", "IT", "Mechanical", "Civil"])

        # Create Teacher profile
        teacher = Teacher.objects.create(
            user=user,
            name=full_name,
            enrollment_number=generate_unique_enrollment_number(),
            department=department,  # Random department
            phone_number=f"+91-{random.randint(6000000000, 9999999999)}",  # Random Indian phone number
            bio=f"Teacher in {department}",  # Bio based on department
            security_key="teacher",  # Default security key
            is_approved=False,  # Not approved by default
        )

        print(f"Created teacher: {teacher}")

# Call this function to generate a specific number of teachers
 # Example: creating 5 teachers
