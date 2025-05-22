from django.db import models


class CompanyModelManager(models.Manager):

    def bulk_create_with_employees(self, parent_list: list):
        companies = [Company(company_name=parent['company_name']) for parent in parent_list]
        employees = [elm | {'parent_name': parent['company_name']} for parent in parent_list for elm in parent['employees']]
        Company.objects.bulk_create(companies, batch_size=500)
        company_map = {company.company_name: company for company in companies}
        employees = [
            Employee(
                company=company_map[employee.pop('parent_name')],
                **employee
            )
            for employee in employees
        ]
        Employee.objects.bulk_create(employees, batch_size=500)
        return companies


class Company(models.Model):
    company_name = models.CharField(max_length=150, unique=True)
    objects = CompanyModelManager()

    def __str__(self):
        return self.company_name


class Employee(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='employees',
                                related_query_name='employee')
    employee_id = models.PositiveIntegerField(unique=True)
    manager_id = models.PositiveIntegerField()
    department_id = models.PositiveIntegerField()
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=12)
    salary = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return '%s %s' % (self.first_name, self.last_name)
