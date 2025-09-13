import logging
from django.core.management import call_command
from django.conf import settings
from celery import shared_task
from custom_exceptions.exceptions import NoUserIsFoundException
from .task_functions import (pdf_result_return, save_pdf, 
text_result_return, save_text)

@shared_task(bind=True)
def execute_elastic_search_cmd(*args, **kwargs):
    call_command('search_index', '--rebuild', '-f')


@shared_task(bind=True)
def download_pdf(self, data: dict):
    try:
        pdf_result = pdf_result_return(data)
        data_bytes, _, file_name = pdf_result
        save_pdf(bytes(data_bytes), file_name)
        return f"{settings.MEDIA_ROOT}pdf/{file_name}"
    except (TypeError, ValueError) as e:
        logging.error(e)
    except (NoUserIsFoundException) as e:
        logging.error(e)

@shared_task(bind=True)
def download_text(self, data: dict):
    try:
        txt_result = text_result_return(data)
        data_txt, _, file_name = txt_result
        save_text(str(data_txt), file_name)
        return f"{settings.MEDIA_ROOT}text/{file_name}"
    except (TypeError, ValueError) as e:
        logging.error(e)
    except (NoUserIsFoundException) as e:
        logging.error(e)



