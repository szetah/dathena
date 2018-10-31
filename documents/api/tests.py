from io import StringIO

from django.contrib.auth.models import User
from django.core.management import call_command
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from ..models import Document


class DocumentAPIViewTestCase(APITestCase):
    """
    Test generic functions for the Documents API

    Ryan, 30.10.2018
    """

    def setUp(self):
        """
        Initial setup

        Ryan, 30.10.2018
        """
        super().setUp()

        call_command('loaddata', 'document_initial_data.json')

        self.user = User.objects.create_user('admin', 'admin@test.com', 'pass')

    def generate_gif(self):
        """
        Generate dummy gif file
        """
        dummy_file = StringIO(
            'GIF87a\x01\x00\x01\x00\x80\x01\x00\x00\x00\x00ccc,\x00'
            '\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00;'
        )
        dummy_file.name = 'test_img_file.gif'
        return dummy_file

    def upload_document(self, update_context={}):
        """
        Upload a document
        """
        test_data = {
            'file': self.generate_gif(),
            'language': 'en',
            'document_type': 'others',
            'confidentiality': 'public',
            'user': 'admin'
        }

        if update_context:
            test_data.update(update_context)

        response = self.client.put(
            reverse('documents:upload'),
            test_data,
            format='multipart'
        )
        return response

    def test_upload_document(self):
        """
        Test function to upload a document
        """

        upload_document_url = reverse('documents:upload')

        # test bad request insufficient data
        test_data = {
            'file': self.generate_gif()
        }

        response = self.client.put(
            upload_document_url,
            test_data,
            format='multipart'
        )
        self.assertEqual(response.data['status'], status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Document.objects.all().count(), 0)

        # test invalid username
        test_data = {
            'file': self.generate_gif(),
            'language': 'en',
            'document_type': 'others',
            'confidentiality': 'public',
            'user': 'test_user'
        }

        response = self.client.put(
            upload_document_url,
            test_data,
            format='multipart'
        )
        self.assertEqual(response.data['status'], status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Document.objects.all().count(), 0)

        # test with complete data
        response = self.upload_document()
        self.assertEqual(response.data['status'], status.HTTP_202_ACCEPTED)
        self.assertEqual(Document.objects.all().count(), 1)

    def test_rud_document(self):
        """
        Test function to retrieve, update and delete a document
        """

        # upload a documnet
        self.upload_document()

        # retrieve document PK to test
        test_document = Document.objects.all().first()

        # test retrive document with invvalid pk
        rud_document_url = reverse(
            'documents:document',
            kwargs={'pk': 99}
        )
        response = self.client.get(
            rud_document_url,
        )
        self.assertEqual(response.status_code, 404)

        # test update document with invvalid pk
        response = self.client.patch(
            rud_document_url,
            {
                'language': 'af',
                'document_type': 'pdf'
            }
        )
        self.assertEqual(response.status_code, 404)

        # test delete document with invvalid pk
        response = self.client.delete(
            rud_document_url
        )
        self.assertEqual(response.status_code, 404)

        # test retrieve document with pk
        rud_document_url = reverse(
            'documents:document',
            kwargs={'pk': test_document.pk}
        )
        response = self.client.get(
            rud_document_url,
        )
        self.assertEqual(response.status_code, 200)

        # test update document with pk
        rud_document_url = reverse(
            'documents:document',
            kwargs={'pk': test_document.pk}
        )
        response = self.client.patch(
            rud_document_url,
            {
                'language': 'af',
                'document_type': 'pdf'
            }
        )
        test_document.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(test_document.language.short_name, 'af')
        self.assertEqual(test_document.document_type.short_name, 'pdf')
        self.assertEqual(Document.objects.all().count(), 1)

        # test delete document with pk
        rud_document_url = reverse(
            'documents:document',
            kwargs={'pk': test_document.pk}
        )
        response = self.client.delete(
            rud_document_url
        )
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Document.objects.all().count(), 0)

    def test_search_document(self):
        """
        Test search document API by tags
        """

        # upload a documnet
        self.upload_document()

        # init search document url
        search_document_url = reverse('documents:search')

        # search without any criteria
        response = self.client.post(
            search_document_url
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['data']), 0)

        # search with confidentiality
        response = self.client.post(
            search_document_url,
            {
                'confidentiality': 'public'
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['data']), 1)

        response = self.client.post(
            search_document_url,
            {
                'confidentiality': 'private'
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['data']), 0)

        # test search with default tag
        response = self.client.post(
            search_document_url,
            {
                'keywords': "private, topsecret, internal"
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['data']), 0)

        # test search with default tag
        response = self.client.post(
            search_document_url,
            {
                'keywords': "private, public, topsecret, internal"
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['data']), 1)

        # upload another documnet
        self.upload_document(update_context={
            'language': 'ms',
            'document_type': 'powerpoint',
            'confidentiality': 'secret',
            'tags': ['2018', 'tax', 'audit', 'account', ]
        })

        # test search with default tag
        response = self.client.post(
            search_document_url,
            {
                'keywords': "secret, public"
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['data']), 2)

        response = self.client.post(
            search_document_url,
            {
                'keywords': "tax"
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['data']), 1)
