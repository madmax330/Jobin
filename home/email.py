
from django.core.mail import EmailMultiAlternatives

# mail accounts


def send_email(to, subject, template, text_content):
    from_email = 'notifications@jobin.com'
    msg = EmailMultiAlternatives(subject, text_content, from_email,  [to])
    msg.attach_alternative(template, "text/html")
    msg.send()