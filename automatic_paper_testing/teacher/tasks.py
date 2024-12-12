from celery import shared_task
from django.utils.timezone import now
from .models import Exam


@shared_task
def update_exam_visibility():
    """Check all exams and update visibility based on start and end times."""
    current_time = now()
    exams_to_start = Exam.objects.filter(start_time__lte=current_time, end_time__gte=current_time)
    exams_to_close = Exam.objects.filter(end_time__lt=current_time)

    # Start exams
    for exam in exams_to_start:
        if not exam.is_active():
            exam.start_exam()

    # Close exams
    for exam in exams_to_close:
        exam.close_exam()
