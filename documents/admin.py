from django.contrib import admin

from .models import (
    Confidentiality,
    Document,
    DocumentType,
    Language,
)


@admin.register(Confidentiality)
class ConfidentialityAdmin(admin.ModelAdmin):
    list_display = [
        'pk',
        'name',
        'short_name',
        'authority_level',
        'total_docs',
    ]


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = [
        'pk',
        'confidentiality',
        'language',
        'document_type',
        'file',
        'user',
        'tags',
    ]


@admin.register(DocumentType)
class DocumentTypeAdmin(admin.ModelAdmin):
    list_display = [
        'pk',
        'name',
        'short_name',
        'total_docs',
    ]


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = [
        'pk',
        'name',
        'short_name',
        'total_docs',
    ]
