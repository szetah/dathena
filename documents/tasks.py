# from celery.task.schedules import crontab
from celery import shared_task
from celery.utils.log import get_task_logger


from .models import (
    Confidentiality,
    Document,
    DocumentType,
    Language,
)

logger = get_task_logger(__name__)


@shared_task
def count_total_docs():
    count_confidentiality()
    count_language()
    count_document_type()


def count_confidentiality():
    for this_confidentiality in Confidentiality.objects.all():
        counts = Document.objects.filter(confidentiality=this_confidentiality).count()
        this_confidentiality.total_docs = counts
        this_confidentiality.save(update_fields=['total_docs', ])


def count_language():
    for this_language in Language.objects.all():
        counts = Document.objects.filter(language=this_language).count()
        this_language.total_docs = counts
        this_language.save(update_fields=['total_docs', ])


def count_document_type():
    for this_document_type in DocumentType.objects.all():
        counts = Document.objects.filter(document_type=this_document_type).count()
        this_document_type.total_docs = counts
        this_document_type.save(update_fields=['total_docs', ])
