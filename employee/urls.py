from .views import BulkEmployeeFileViewSet
from django.urls import path


urlpatterns = [
    path('upload-employees/', BulkEmployeeFileViewSet.as_view(), name='upload-employees-excel'),
]
