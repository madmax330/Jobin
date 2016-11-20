from itsdangerous import URLSafeTimedSerializer
from django.forms.models import model_to_dict
from home import apps


def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer('Job_in')
    return serializer.dumps(email, salt='Job_in_pass')


def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer('Job_in')
    try:
        email = serializer.loads(
            token,
            salt='Job_in_pass',
            max_age=expiration
        )
    except:
        raise Exception("Boo!")
    return email