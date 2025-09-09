import os
from django.core.management import call_command
from jwt import decode as jwt_decode
from jwt import (InvalidTokenError, InvalidSignatureError,
                DecodeError, ExpiredSignatureError)
from django.conf import settings
from celery import shared_task
from note.pdf_downloader.downloader import download_pdf as pdf
from note.push_websocket import file_downloading_send_notification
from custom_exceptions.exceptions import NoUserIsFoundException


@shared_task(bind=True)
def execute_elastic_search_cmd(*args, **kwargs):
    call_command('search_index', '--rebuild', '-f')


def token_checker(token: str):
    try:
        signing_key = settings.SIMPLE_JWT.get('SIGNING_KEY')
        if signing_key is None:
            raise ValueError("No signing key is found.")
        data = jwt_decode(token, signing_key, algorithms=["HS256"])
        return data['user_id']
    except (TypeError, ValueError, InvalidTokenError,
           InvalidSignatureError, ExpiredSignatureError, DecodeError) as e:
        return e
    
def validate_user(data: dict):
    try:
        user_id = token_checker(str(data.get('user_access_token')))
        if str(user_id) != str(data.get('auth_user_id')):
            raise NoUserIsFoundException("No user was found or logged during PDF generation.")
        return user_id
    except(ValueError, TypeError) as e:
        return e

def generate_pdf(data: dict, user_id: str):
    try:
        name = data.get("name")
        html_content = data.get("html_content")
        return pdf(str(name), str(html_content), user_id)
    except(ValueError, TypeError) as e:
        return e

def notification_websocket_download(file_type: str, user_id: str):
     file_downloading_send_notification(
     instance=f"{file_type} file is downloading, please wait...", user_id=user_id
     )

def save_pdf(pdf_data: bytes, file_name: str):
    try:
        os.makedirs(f"{settings.MEDIA_ROOT}pdf/", exist_ok=True)
        file_path = os.path.join(f"{settings.MEDIA_ROOT}pdf/", file_name)
        with open(file_path, "wb") as f:
            f.write(pdf_data)
        return file_path
    except OSError as e:
        return e

@shared_task(bind=True)
def download_pdf(self, data: dict):
    try:
        user_id = validate_user(data)
        notification_websocket_download('PDF', str(user_id))
        pdf_result = generate_pdf(data, str(user_id))
        if isinstance(pdf_result, (ValueError, TypeError)):
            raise pdf_result
        data_bytes, _, file_name = pdf_result
        save_pdf(bytes(data_bytes), file_name)
        return f"{settings.MEDIA_ROOT}pdf/{file_name}"
    except (TypeError, ValueError) as e:
        raise self.retry(exc=e, countdown=10, max_retries=3)
    except (NoUserIsFoundException):
         return {'status': 'FAILURE', 'error': 'User is not found or not logged in.'}

