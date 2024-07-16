"""
URL configuration for HR project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path , include
from Employee import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', views.user_login, name='login'),
    path('add-expenses/', views.add_expenses, name='add_expenses'),
    path('generate-pdf/', views.generate_pdf, name='generate_pdf'),
    path('employee/update/<str:emp_id>/', views.employee_update, name='employee_update'),
    # path('employee_update/<str:emp_id>/',views.employee_update,name='employee_update'),
    path('salarysheet/', views.salarysheet, name='salarysheet'),

    path('salarysheet',views.salarysheet,name='salary_sheet'),
    path('salarysheet/', views.salarysheet, name='salarysheet'),
    
    path('dashboard/', views.dashboard, name='dashboard'),
    path('leavetable/', views.leavetable, name='leavetable'),
    path('add_emp',views.add_emp,name='add_emp'),
    path('logout',views.logout),
    path('emp_dashboard',views.emp_dashboard,name='emp_dashboard'),
    path('emp_attend',views.emp_attend,name='emp_attend'),
    path('emp_leave',views.emp_leave,name = 'emp_leave'),
    path('view_emp',views.view_emp,name='view_emp'),
    path('emp_details',views.emp_details,name ='emp_details'),
    # path('generate_salary/', views.generate_salary, name='generate_salary'),
    path('emp_leavetable/<str:emp_id>/', views.emp_leavetable, name='emp_leavetable'),
    path('view_all/<str:emp_id>/', views.view_all, name='view_all'),
    path('add_holiday/', views.add_holiday, name='add_holiday'),
    path('holiday_list/', views.holiday_list, name='holiday_list'),
    path('get-previous-leave-dates/', views.get_previous_leave_dates, name='get_previous_leave_dates'),
    path('emp_leavetable/<str:emp_id>/', views.emp_leavetable, name='emp_leavetable'),
    path('logout/', views.user_logout, name='user_logout'),
    path('leave_requests/', views.leave_request_list, name='leave_request_list'),
    path('leave_requests/<int:pk>/', views.leave_request_detail, name='leave_request_detail'),
    path('leave_requests/<int:pk>/approve/', views.approve_leave_request, name='approve_leave_request'),
    path('leave_requests/<int:pk>/<str:status>/', views.leave_request_detail, name='leave_request_detail'),
    path('download_employee_details/<str:emp_id>/', views.download_employee_details, name='download_employee_details'),
    path('HR_update/', views.HR_update, name='HR_update'),
    path('update_outtime/<int:attendance_id>/', views.update_outtime, name='update_outtime'),
    path('emp_info',views.emp_info,name='emp_info'),
    path('add_company/', views.add_company, name='add_company'),
    path('company_list', views.company_list, name='company_list'),
    path('WFHODForm', views.wfhod_form, name='WFHODForm'),
    path('get_notifications/', views.get_notifications, name='get_notifications'),
    path('employee/<str:emp_id>/leave_balance/', views.employee_leave_balance, name='employee_leave_balance'),
    path('generate_pdf/<str:emp_id>/', views.generate_pdf, name='generate_pdf'),
    path('upload/', views.upload_salary_slip, name='upload_salary_slip'),
    path('upload_success/', views.upload_success, name='upload_success'),
    path('employee/salary/<str:emp_id>/', views.salary_detail, name='salary'),
    # path('view/<int:emp_id>/', views.view_salary_slips, name='view_salary_slips'),
    path('view/<str:emp_id>/', views.view_salary_slips, name='view_salary_slips'),
    path('salary-slips/', views.salary_slip_overview, name='salary_slip_overview'),
    path('salary-slip/<str:salary_slip_id>/', views.view_salary_slip, name='view_salary_slip'),
    path('small_report/<str:emp_id>/', views.small_report, name='small_report'),
    path('view_expenses/', views.view_expenses, name='view_expenses'),
    path('employee/<str:emp_id>/leave_balance/csv/', views.employee_leave_balance_csv, name='employee_leave_balance_csv'),
    path('download_csv/', views.download_csv, name='download_csv'),
    path('pdf_generate/<str:emp_id>/', views.pdf_generate, name='pdf_generate'),
    path('pdf_upload/<str:emp_id>/', views.pdf_upload, name='pdf_upload'),
    path('hrUpdateOutime/', views.hrUpdateOutime, name='hrUpdateOutime'),
    path('updateattend',views.updateattend,name='updateattend'),
    

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
handler403 = 'Employee.views.handle_permission_denied'

