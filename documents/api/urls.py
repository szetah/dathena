from django.urls import path

from .views import (
    DocumentSearchView,
    DocumentUploadView,
    DocumentRUDView,
)


app_name = 'documents'

urlpatterns = [
    path(
        '<int:pk>/',
        DocumentRUDView.as_view(),
        name='document'
    ),
    path(
        'upload/',
        DocumentUploadView.as_view(),
        name='upload',
    ),
    path(
        'search/',
        DocumentSearchView.as_view(),
        name='search',
    ),
]
