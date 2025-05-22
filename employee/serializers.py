from .models import Employee, Company
from django.core.validators import FileExtensionValidator
from rest_framework import serializers


class EmployeeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Employee
        fields = ['employee_id', 'first_name', 'last_name', 'phone_number', 'salary', 'manager_id', 'department_id']


class CompanyBulkCreateSerializer(serializers.ListSerializer):
    def create(self, validated_data):
        return Company.objects.bulk_create_with_employees(validated_data)


class CompanySerializer(serializers.ModelSerializer):
    employees = EmployeeSerializer(many=True)

    class Meta:
        model = Company
        fields = ['company_name', 'employees']
        list_serializer_class = CompanyBulkCreateSerializer


class FileFormSerializer(serializers.Serializer):
    file_upload = serializers.FileField(validators=[FileExtensionValidator(['xlsx', 'xls'])])

    class Meta:
        fields = ['file_upload']
