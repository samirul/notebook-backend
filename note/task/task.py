import os
from django.core.management import call_command
from jwt import decode as jwt_decode
from jwt import (InvalidTokenError, InvalidSignatureError,
                DecodeError, ExpiredSignatureError)
from django.conf import settings
from celery import shared_task
from note.pdf_downloader.downloader import download_pdf as pdf
from note.push_websocket import file_downloading_send_notification


@shared_task(bind=True)
def execute_elastic_search_cmd(*args, **kwargs):
    call_command('search_index', '--rebuild', '-f')


def token_checker(token: str):
    try:
        SIGNING_KEY = settings.SIMPLE_JWT.get('SIGNING_KEY')
        if SIGNING_KEY is None:
            raise ValueError("No signing key is found.")
        data = jwt_decode(token, SIGNING_KEY, algorithms=["HS256"])
        return data['user_id']
    except (TypeError, ValueError, InvalidTokenError,
           InvalidSignatureError, ExpiredSignatureError, DecodeError) as e:
        return e
    
class NoUserIsFoundException(Exception):
    pass


def validate_user(data: dict):
    user_id = token_checker(data.get('user_access_token'))
    if str(user_id) != str(data.get('auth_user_id')):
        raise NoUserIsFoundException("No user was found or logged during PDF generation.")
    return user_id

def generate_pdf(data: dict, user_id: str):
    name = data.get("name")
    html_content = data.get("html_content")
    return pdf(name, html_content, user_id)

def notification_websocket_download(file_type: str, user_id: str):
     file_downloading_send_notification(
     instance=f"{file_type} file is downloading, please wait...", user_id=user_id
     )

def save_pdf(pdf_data: bytes, file_name: str):
    os.makedirs(f"{settings.MEDIA_ROOT}pdf/", exist_ok=True)
    file_path = os.path.join(f"{settings.MEDIA_ROOT}pdf/", file_name)
    with open(file_path, "wb") as f:
        f.write(pdf_data)
    return file_path

@shared_task(bind=True)
def download_pdf(self, data):
    try:
        user_id = validate_user(data)
        notification_websocket_download('PDF', user_id)
        data, _, file_name = generate_pdf(data, user_id)
        save_pdf(data, file_name)
        return f"{settings.MEDIA_ROOT}pdf/{file_name}"
    except (TypeError, ValueError) as e:
        raise self.retry(exc=e, countdown=10, max_retries=3)
    except (InvalidTokenError, InvalidSignatureError,
           ExpiredSignatureError, DecodeError, NoUserIsFoundException):
         return {'status': 'FAILURE', 'error': 'User is not found or not logged in.'}

