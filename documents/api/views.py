from django.utils.translation import ugettext_lazy as _
from django.db.models import Q

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import (
    GenericAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.mixins import ListModelMixin

from .serializers import DocumentSerializer
from ..models import Document


class DocumentUploadView(APIView):
    """
    An endpoint to upload a Document

    Ryan, 30.10.2018
    """

    serializer_class = DocumentSerializer

    def put(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()

            message = _("Document Uploaded!")
            data = serializer.data
            http_status = status.HTTP_202_ACCEPTED
        else:
            message = _("Error!"),
            data = serializer.errors,
            http_status = status.HTTP_400_BAD_REQUEST

        return Response({
            "message": message,
            "data": data,
            "status": http_status,
        })


class DocumentRUDView(RetrieveUpdateDestroyAPIView):
    """
    An endpoint to retriev, update or delete a Document

    Ryan, 30.10.2018
    """

    lookup_field = 'pk'
    serializer_class = DocumentSerializer
    queryset = Document.objects.all()


class DocumentSearchView(GenericAPIView, ListModelMixin):
    """
    An endpoint to search Document via tags

    Ryan, 30.10.2018
    """
    serializer_class = DocumentSerializer

    def get_initial_queryset(self):
        """
        Get initial queryset of document list if criteria is passed
        """
        self.queryset = Document.objects.none()

        if (
            self.request.data.get('confidentiality', None) or
            self.request.data.get('language', None) or
            self.request.data.get('document_type', None) or
            self.request.data.get('keywords', '')
        ):
            self.queryset = Document.objects.all()

            if self.request.data.get('confidentiality', None):
                self.queryset = self.queryset.filter(
                    confidentiality__short_name=self.request.data['confidentiality']
                )

            if self.request.data.get('language', None):
                self.queryset = self.queryset.filter(
                    language__short_name=self.request.data['language']
                )

            if self.request.data.get('document_type', None):
                self.queryset = self.queryset.filter(
                    document_type__short_name=self.request.data['document_type']
                )

        return self.queryset

    def validate_keywords(self):
        """
        Convert a string by separated with comma, strip, and convert into list
        """
        return [keyword.strip() for keyword in self.request.data['keywords'].split(',')]

    def get_queryset(self):
        """
        Get queryset of the keywords search
        """
        self.queryset = self.get_initial_queryset()

        if self.request.data.get('keywords', ''):

            keywords = self.validate_keywords()
            self.q_objects = Q()

            # dynamic generate Q query with kewords
            for keyword in keywords:
                self.q_objects.add((Q(tags__icontains=keyword)), self.q_objects.OR)

            self.queryset = self.queryset.filter(self.q_objects)

        return self.queryset

    def post(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        response = {
            'message': _("List of Documents"),
            'status': status.HTTP_200_OK,
            'data': serializer.data
        }
        return Response(response, status=response['status'])
