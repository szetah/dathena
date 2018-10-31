from django.contrib.auth.models import User

from rest_framework import serializers


from ..models import (
    Confidentiality,
    Document,
    DocumentType,
    Language,
)


class ConfidentialitySerializer(serializers.ModelSerializer):
    """
    Serializer for Confidentiality class.

    @Ryan, 29.10.2018
    """

    class Meta:
        model = Confidentiality
        fields = (
            'name',
            'short_name',
            'authority_level',
            'total_docs'
        )
        read_only_fields = (
            'pk',
            'created',
            'modified',
        )


class LanguageSerializer(serializers.ModelSerializer):
    """
    Serializer for Language class.

    @Ryan, 29.10.2018
    """

    class Meta:
        model = Language
        fields = (
            'name',
            'short_name',
            'total_docs'
        )
        read_only_fields = (
            'pk',
            'created',
            'modified',
        )


class DocumentTypeSerializer(serializers.ModelSerializer):
    """
    Serializer for DocumentType class.

    @Ryan, 29.10.2018
    """

    class Meta:
        model = DocumentType
        fields = (
            'name',
            'short_name',
            'total_docs',
        )
        read_only_fields = (
            'pk',
            'created',
            'modified',
        )


class DocumentSerializer(serializers.ModelSerializer):
    """
    Serializer for Document class.

    @Ryan, 29.10.2018
    """

    confidentiality = serializers.SlugRelatedField(
        queryset=Confidentiality.objects.all(),
        slug_field='short_name',
    )
    language = serializers.SlugRelatedField(
        queryset=Language.objects.all(),
        slug_field='short_name',
    )
    document_type = serializers.SlugRelatedField(
        queryset=DocumentType.objects.all(),
        slug_field='short_name',
    )
    user = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username',
    )
    tags = serializers.ListField(
        child=serializers.CharField()
    )

    class Meta:
        model = Document
        fields = (
            'confidentiality',
            'language',
            'document_type',
            'file',
            'user',
            'tags'
        )
        read_only_fields = (
            'pk',
            'created',
            'modified',
        )
