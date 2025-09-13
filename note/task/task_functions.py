import os
from jwt import decode as jwt_decode
from jwt import (InvalidTokenError, InvalidSignatureError,
                DecodeError, ExpiredSignatureError)
from django.conf import settings
from note.pdf_downloader.downloader import download_pdf as pdf
from note.text_cleaner.cleaner import CleanHTML
from note.push_websocket import file_downloading_send_notification
from custom_exceptions.exceptions import NoUserIsFoundException


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
    user_id = token_checker(str(data.get('user_access_token')))
    if str(user_id) != str(data.get('auth_user_id')):
        raise NoUserIsFoundException("No user was found or logged during PDF generation.")
    return user_id

def notification_websocket_download(file_type: str, user_id: str):
     file_downloading_send_notification(
     instance=f"{file_type} file is downloading, please wait...", user_id=user_id
     )

##################################################################################################
                                # PDF Generator and downloader
##################################################################################################

def generate_pdf(data: dict, user_id: str):
    name = data.get("name")
    html_content = data.get("html_content")
    return pdf(str(name), str(html_content), user_id)


def save_pdf(pdf_data: bytes, file_name: str):
    try:
        os.makedirs(f"{settings.MEDIA_ROOT}pdf/", exist_ok=True)
        file_path = os.path.join(f"{settings.MEDIA_ROOT}pdf/", file_name)
        with open(file_path, "wb") as f:
            f.write(pdf_data)
        return file_path
    except PermissionError as e:
        return e
    
def pdf_result_return(data: dict):
    user_id = validate_user(data)
    notification_websocket_download('PDF', str(user_id))
    pdf_result = generate_pdf(data, str(user_id))
    if isinstance(pdf_result, (ValueError, TypeError)):
        raise pdf_result
    return pdf_result


##################################################################################################
                                # Text Generator and downloader
##################################################################################################

def clean_text(html_content: str):
    return CleanHTML(html_content).filtered_result()

def generate_text(data: dict, user_id: str):
    cleaned_html  = clean_text(str(data.get("html_content")))
    content_type="application/text"
    file_name = f"{data.get("name")}_{user_id}_output.txt"
    return cleaned_html, content_type, file_name


def save_text(pdf_data: str, file_name: str):
    try:
        os.makedirs(f"{settings.MEDIA_ROOT}text/", exist_ok=True)
        file_path = os.path.join(f"{settings.MEDIA_ROOT}text/", file_name)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(pdf_data)
        return file_path
    except PermissionError as e:
        return e

def text_result_return(data: dict):
    user_id = validate_user(data)
    notification_websocket_download('Text', str(user_id))
    return generate_text(data, str(user_id))