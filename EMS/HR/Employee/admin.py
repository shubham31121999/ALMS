from django.contrib import admin
from .models import Employee,Attendance,LeaveRequest,Company,SalaryDetails,TravelExpense,Receipt
# Register your models here.



admin.site.register(Employee)
admin.site.register(Attendance)
admin.site.register(LeaveRequest)
admin.site.register(Company)
admin.site.register(SalaryDetails)
admin.site.register(TravelExpense)
admin.site.register(Receipt)