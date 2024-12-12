from django.conf import settings
from django.core.mail import EmailMessage

def sent_mail(name, gmail, body):

    subject = "Email verification code "
    from_email = settings.EMAIL_HOST_USER
    to = ["eyesofegale01@gmail.com"]
    body = f"Dear {name}\nPlease find your portal access verification code: {body}"
    mail = EmailMessage(subject, body, from_email, to)

    mail.send()