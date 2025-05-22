from rest_framework import generics, status, serializers, parsers
from .serializers import CompanySerializer, FileFormSerializer
from rest_framework.response import Response
from io import BytesIO
import pandas as pd
from drf_spectacular.utils import extend_schema, inline_serializer


@extend_schema(
    request=FileFormSerializer,
    responses={201: CompanySerializer},
    methods=["POST"]
)
class BulkEmployeeFileViewSet(generics.CreateAPIView):
    serializer_class = CompanySerializer
    parser_classes = [parsers.MultiPartParser]


    def create(self, request, *args, **kwargs):
        excel_file = request.FILES.get('file_upload')
        file_serializer = FileFormSerializer(data=request.data)
        if file_serializer.is_valid(raise_exception=True):
            df = pd.read_excel(BytesIO(excel_file.read()))
            df.rename(columns=str.lower, inplace=True)
            df = df.groupby('company_name').apply(
                lambda x: x[['employee_id', 'first_name', 'last_name', 'phone_number', 'salary', 'manager_id',
                             'department_id']].to_dict('records')
            ).to_frame('employees').reset_index()
            response = df.to_dict('records')
            serializer = self.get_serializer(data=response, many=True)
            serializer.is_valid(raise_exception=True)
            try:
                self.perform_create(serializer)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

    def get_serializer(self, *args, **kwargs):
        if isinstance(kwargs.get("data", {}), list):
            kwargs["many"] = True
        return super(BulkEmployeeFileViewSet, self).get_serializer(*args, **kwargs)
