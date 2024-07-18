from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.utils import timezone
from django.db import transaction
from .models import Employee, SalaryDetails
from datetime import datetime
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.exceptions import ValidationError
# from .utils import generate_salary_pdf
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from .forms import EmployeeAttendanceForm
from .models import Employee,Attendance ,SalaryDetails
from .models import SalaryDetails
from .models import Employee, LeaveRequest, Attendance, Holiday
from .forms import EmployeeCreationForm,LeaveRequestForm,OutTimeUpdateForm
from .forms import LoginForm,AttendanceForm,CompanyForm,TimeUpdateForm
from .models import LeaveRequest,Company
from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render, redirect , get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.contrib.auth import update_session_auth_hash
from django.http import JsonResponse
from django.utils.dateparse import parse_time
from datetime import datetime, timedelta
from datetime import time
from datetime import date
from django.shortcuts import render, redirect
from .models import LeaveRequest
from .forms import LeaveRequestApprovalForm
import csv
from .forms import HolidayForm
from .models import Holiday,userCompany
from django.db.models import Count
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import EmployeeCreationForm,WFHODForm
from .models import Company, Employee
from django.http import JsonResponse
from openpyxl import Workbook
from .forms import ProfileUpdateForm
from django.contrib.auth.hashers import make_password
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.units import inch
from django.http import HttpResponse
from io import BytesIO
from django.template.defaultfilters import slugify
from django.contrib.auth import logout as auth_logout
# Create your views here.


from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied
from django.shortcuts import render

from .models import Holiday
# from .forms import TravelExpenseForm , TravelExpenseFormSet
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Image
from reportlab.lib.utils import ImageReader
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import TravelExpense

from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

from django.contrib.auth.models import User
from .models import Employee
import os 
#TravelExpenseFormSet = modelformset_factory(TravelExpense, form=TravelExpenseForm, extra=2, can_delete=True, max_num=1)
from .models import ExpenseReport
from django.core.files.base import ContentFile
import tempfile
import os

from django.shortcuts import render
from django.http import JsonResponse
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from datetime import datetime
import os
import tempfile

# views.py
from django.shortcuts import render
from .models import Employee, SalaryDetails





# from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from .models import Employee,SalaryDetails


from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render, redirect
from .models import SalaryDetails


from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError
from .models import SalaryDetails
import datetime
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.conf import settings
import os
import zipfile
from io import BytesIO
from reportlab.pdfgen import canvas
from .models import Employee, SalaryDetails

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.core.exceptions import ValidationError
from datetime import datetime
from .models import Employee, SalaryDetails, Company, SalarySlip  # Ensure Company model is imported


from django.shortcuts import render, redirect
from .models import Attendance
from .forms import OutTimeUpdateForm
from django.utils import timezone
from datetime import datetime

from django.shortcuts import render, redirect, get_object_or_404
from .models import Attendance, Company
from .forms import TimeUpdateForm,HRAttendance

# views.py



# views.py

# views.py

from django.shortcuts import render, redirect
from .models import Employee, Attendance
from .forms import AttendanceForm

def updateattend(request):
    employees = Employee.objects.all()
    if request.method == 'POST':
        for employee in employees:
            form = AttendanceForm(request.POST, prefix=f'employee_{employee.id}')
            if form.is_valid():
                # Save attendance for each employee
                attendance = form.save(commit=False)
                attendance.employee = employee
                attendance.save()
            else:
                # Handle form errors appropriately
                pass

        # Redirect to a success page or refresh the current page
        return redirect('updateattend')  # Replace with your URL name

    else:  # GET request
        formset = []
        for employee in employees:
            attendance_instance = Attendance(employee=employee)  # Create a dummy instance of Attendance
            form = AttendanceForm(instance=attendance_instance, prefix=f'employee_{employee.id}')
            formset.append(form)

        context = {
            'formset': formset,
        }
        return render(request, 'hr_temp/updateattend.html', context)



def addUserCompany(request):
    if request.method == 'POST':
        # Extract data from the POST request
        com_id = request.POST.get('comId')
        com_name = request.POST.get('comName')
        com_gst = request.POST.get('comGST')
        com_cin = request.POST.get('comCIN')
        com_cont = request.POST.get('comCont')
        com_email = request.POST.get('comEmail')
        com_dl_num1 = request.POST.get('comDLNum1')
        com_dl_num2 = request.POST.get('comDLNum2')
        com_pan_num = request.POST.get('comPanNum')
        com_add = request.POST.get('comAdd')
        com_city = request.POST.get('comCity')
        com_state = request.POST.get('comState')
        com_pin = request.POST.get('comPin')
        
        # Create a new userCompany object and save it to the database
        new_company = userCompany(
            comId=com_id,
            comName=com_name,
            comGST=com_gst,
            comCIN=com_cin,
            comCont=com_cont,
            comEmail=com_email,
            comDLNum1=com_dl_num1,
            comDLNum2=com_dl_num2,
            comPanNum=com_pan_num,
            comAdd=com_add,
            comCity=com_city,
            comState=com_state,
            comPin=com_pin
        )
        new_company.save()
        
        # Redirect to a success page or any other logic after successful form submission
        return redirect('addUserCompany')  # Replace 'success_url_name' with the name of your success URL pattern
    
    # If the request method is not POST, render the form template (GET request)
    return render(request, 'hr_temp/addUserCompany.html')




def hrUpdateOutime(request):
    # Fetch all attendance records initially
    attendance_records = Attendance.objects.filter(intime__isnull=False, outtime__isnull=True)

    # Handle filtering by company name if provided in GET parameters
    company_name = request.GET.get('company')
    if company_name and company_name != 'All Companies':
        attendance_records = attendance_records.filter(employee__company__company_name=company_name)

    if request.method == "POST":
        form = TimeUpdateForm(request.POST)
        
        if form.is_valid():
            employee_id = form.cleaned_data['employee']
            date = form.cleaned_data['date']
            outtime = form.cleaned_data['outtime']
            
            try:
                # Retrieve Attendance object using get_object_or_404 or filter
                attendance_record = Attendance.objects.get(employee_id=employee_id, date=date)
                attendance_record.outtime = outtime
                attendance_record.save()
                return redirect('hrUpdateOutime')
            except Attendance.DoesNotExist:
                print(f"Attendance record not found for employee_id={employee_id} and date={date}")
                # Handle case where Attendance record does not exist
                # Optionally, you can redirect or render a specific error message
        else:
            print(form.errors)
    else:
        form = TimeUpdateForm()

    # Fetch all companies to populate the filter dropdown
    companies = Company.objects.all()

    context = {
        'attendance_records': attendance_records,
        'form': form,
        'companies': companies,
        'selected_company': company_name  # Pass the selected company name to the template
    }
    return render(request, 'hr_temp/hrUpdateOutime.html', context)




















def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def generate_salary_pdf(request):
    # Create a buffer to store PDF content
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    user = request.user
    employee = Employee.objects.get(user=user)
    salary_details = SalaryDetails.objects.filter(employee=employee).latest('month')
    company = Company.objects.first()

    month_start_date = datetime(salary_details.month.year, salary_details.month.month, 1)
    month_end_date = datetime(salary_details.month.year, salary_details.month.month, calendar.monthrange(salary_details.month.year, salary_details.month.month)[1])
    
    employee_leave_requests = LeaveRequest.objects.filter(employee=employee, status='approved', date__range=(month_start_date, month_end_date))
    
    cl_leaves_taken = employee_leave_requests.filter(leave_type='CL').count()
    sl_leaves_taken = employee_leave_requests.filter(leave_type='SL').count()
    pl_leaves_taken = employee_leave_requests.filter(leave_type='PL').count()

    cl_opening_balance = employee.CL - LeaveRequest.objects.filter(employee=employee, leave_type='CL', date__lt=month_start_date).count()
    sl_opening_balance = employee.SL - LeaveRequest.objects.filter(employee=employee, leave_type='SL', date__lt=month_start_date).count()
    pl_opening_balance = employee.PL - LeaveRequest.objects.filter(employee=employee, leave_type='PL', date__lt=month_start_date).count()
    
    cl_balance = employee.CL - cl_leaves_taken
    sl_balance = employee.SL - sl_leaves_taken
    pl_balance = employee.PL - pl_leaves_taken
    salary_month_year = salary_details.month.strftime('%B %Y')
    # Title for the PDF
    title = f"{employee.company.company_name}"
    story = [Paragraph(title, styles['Title'])]
    story.append(Paragraph(f"SALARY SLIP FOR THE MONTH OF - {salary_month_year}", styles['Title']))
    
    net_salary = salary_details.net_salary
    net_salary_words = convert_to_words(net_salary)

    # Prepare data for the first table (Employee Information)
    table_data_employee = [
        [ f'Salary for {salary_month_year}','', 'Employee ID', employee.emp_id],
        [Paragraph('<b>Employee Name:</b>', styles['Normal']), Paragraph(f"{employee.user.first_name} {employee.user.last_name}", styles['Normal']),
         Paragraph('<b>Designation:</b>', styles['Normal']), Paragraph(employee.designation, styles['Normal'])],
        [Paragraph('<b>Date of Joining:</b>', styles['Normal']), Paragraph(str(employee.date_of_joining), styles['Normal']),
         Paragraph('<b>Date of Probation:</b>', styles['Normal']), Paragraph(str(employee.date_of_probation), styles['Normal'])],
        [Paragraph('<b>UAN Number:</b>', styles['Normal']), Paragraph(employee.emp_id, styles['Normal']),
         Paragraph('<b>Aadhaar Number:</b>', styles['Normal']), Paragraph(str(employee.aadhaar), styles['Normal'])],
        [Paragraph('<b>PAN Card Number:</b>', styles['Normal']), Paragraph(employee.pan_no, styles['Normal']),
         Paragraph('<b>Bank Name:</b>', styles['Normal']), Paragraph(employee.bank, styles['Normal'])],
        [Paragraph('<b>Account Number:</b>', styles['Normal']), Paragraph(str(employee.bank_account_no), styles['Normal']),
         Paragraph('<b>Date of Birth:</b>', styles['Normal']), Paragraph(str(employee.date_of_birth), styles['Normal'])],
        [Paragraph('<b>Company Name:</b>', styles['Normal']), Paragraph(employee.company.company_name, styles['Normal']), '', '']
    ]

    # Create a table for Employee Information and style
    table_employee = Table(table_data_employee, colWidths=[150, 150, 150, 150], repeatRows=1, hAlign='CENTER')
    table_employee.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
    ]))

    # Add Employee Information table to the story
    story.append(table_employee)

    # Prepare data for the second table (Attendance and Leave Details)
    attendance_data = [
        ['', '', '', '', '', ''],
        [Paragraph('<b>Month Days</b>', styles['Normal']), Paragraph('<b></b>', styles['Normal']),
         Paragraph('<b>Leaves</b>', styles['Normal']), Paragraph('<b>Opening Balance</b>', styles['Normal']),
         Paragraph('<b>Leaves Taken</b>', styles['Normal']), Paragraph('<b>Closing Balance</b>', styles['Normal'])],
        ['Present', salary_details.paid_days, 'Sick Leave', sl_opening_balance, sl_leaves_taken, sl_balance],
        ['Absent', salary_details.absent_days, 'Casual Leave', cl_opening_balance, cl_leaves_taken, cl_balance],
        ['Total', salary_details.total_days, 'Privilege Leave', pl_opening_balance, pl_leaves_taken, pl_balance]
    ]

    # Create a table for Attendance and Leave Details and style
    table_attendance = Table(attendance_data, colWidths=[100, 100, 100, 100, 100, 100], repeatRows=1, hAlign='CENTER')
    table_attendance.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
    ]))

    # Add Attendance and Leave Details table to the story
    story.append(table_attendance)

    # Prepare data for the third table (Salary Details)
    salary_table_data = [
        ['', '', '', '', '', ''],
        [Paragraph('<b>Earnings</b>', styles['Normal']), Paragraph('<b>Standard</b>', styles['Normal']),
         Paragraph('<b>Actual</b>', styles['Normal']), Paragraph('<b>Deductions</b>', styles['Normal']),
         Paragraph('<b>Standard</b>', styles['Normal']), Paragraph('<b>Actual</b>', styles['Normal'])],
        
        ['Basic Pay', salary_details.standard_basic, salary_details.actual_basic, 'PF', salary_details.standard_pf, salary_details.actual_pf],
        ['HRA', salary_details.standard_HRA, salary_details.actual_HRA, 'PT', salary_details.pt_deduction, salary_details.pt_deduction],
        ['Education Allowance', salary_details.standard_edu_allowance, salary_details.actual_edu_allowance, 'LWF', '', salary_details.lw_fund],
        ['Statutory Bonus', salary_details.standard_statutory_bonus, salary_details.actual_statutory_bonus, 'ESIC', '', salary_details.ESIC],
        ['LTA', salary_details.standard_LTA, salary_details.actual_standard_LTA, 'Income Tax', '', salary_details.l_tax],
        ['Loan', '', '', '', '', ''],
        ['Gross Salary', salary_details.gross, '', 'Net Salary', '', salary_details.net_salary],
    ]

    # Create a table for Salary Details and style
    table_salary = Table(salary_table_data, colWidths=[100, 100, 100, 100, 100, 100], repeatRows=1, hAlign='CENTER')
    table_salary.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
    ]))

    # Add Salary Details table to the story
    story.append(table_salary)

    # Add separate table with one column and one row
    one_cell_table_data = [[Paragraph(f'<b>In Words:</b> {net_salary_words} Only', styles['Normal'])]]
    table_one_cell = Table(one_cell_table_data, colWidths=[sum([100, 100, 100, 100, 100, 100])], hAlign='CENTER')
    table_one_cell.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ]))

    # Add the one-cell table to the story
    story.append(Spacer(1, 12))
    story.append(table_one_cell)
    story.append(Spacer(1, 12))

    # Add text below the table
    story.append(Paragraph('This is a computer-generated document. No signature is required.', styles['Normal']))

    # Build PDF
    doc.build(story)

    # Get PDF content from buffer
    pdf_content = buffer.getvalue()
    buffer.close()

    return pdf_content







from django.shortcuts import render, HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from .models import Employee, TravelExpense, Receipt

from datetime import datetime
from PIL import Image as PILImage
from io import BytesIO

def add_expenses(request):
    try:
        user = request.user
        employee = Employee.objects.get(user=user)
    
        if request.method == 'POST':
            # Retrieve POST data for multiple expenses
            sr_nos = request.POST.getlist('sr_no[]')
            from_places = request.POST.getlist('from_place[]')
            from_dates = request.POST.getlist('from_date[]')
            to_places = request.POST.getlist('to_place[]')
            to_dates = request.POST.getlist('to_date[]')
            purposes = request.POST.getlist('purpose[]')
            distances = request.POST.getlist('distance[]')
            models_of_travel = request.POST.getlist('model_of_travel[]')
            food_prices = request.POST.getlist('food_price[]')
            transport_fares = request.POST.getlist('transport_fare[]')
            accommodations = request.POST.getlist('accommodation[]')
            others = request.POST.getlist('other[]')
            miscellaneouses = request.POST.getlist('miscellaneous[]')

            # Initialize a new batch_id for the current batch of expenses
            batch_id = None

            for sr_no, from_place, from_date_str, to_place, to_date_str, purpose, distance, \
                model_of_travel, food_price, transport_fare, accommodation, other, miscellaneous \
                in zip(sr_nos, from_places, from_dates, to_places, to_dates, purposes, distances,
                       models_of_travel, food_prices, transport_fares, accommodations, others, miscellaneouses):

                # Convert date strings to datetime.date objects
                from_date = datetime.strptime(from_date_str, '%Y-%m-%d').date()
                to_date = datetime.strptime(to_date_str, '%Y-%m-%d').date()

                # Handle receipt file uploads
                receipt_files = request.FILES.getlist('receipt_images[]')

                # Create TravelExpense instance
                travel_expense = TravelExpense.objects.create(
                    employee=employee,
                    sr_no=sr_no,
                    from_place=from_place,
                    from_date=from_date,
                    to_place=to_place,
                    to_date=to_date,
                    purpose=purpose,
                    distance=distance,
                    model_of_travel=model_of_travel,
                    food_price=food_price,
                    transport_fare=transport_fare,
                    accommodation=accommodation,
                    other=other,
                    miscellaneous=miscellaneous,
                )

                # Save receipt images and associate with the expense
                for receipt_file in receipt_files:
                    Receipt.objects.create(travel_expense=travel_expense, image=receipt_file)

                # Assign the batch_id to the first created expense in the batch
                if batch_id is None:
                    batch_id = travel_expense.batch_id
                else:
                    travel_expense.batch_id = batch_id
                    travel_expense.save()

            # After all expenses are created in the batch, ensure all have the same batch_id
            TravelExpense.objects.filter(batch_id=None).update(batch_id=batch_id)

            # Generate PDF report
            expenses = TravelExpense.objects.filter(employee=employee, batch_id=batch_id)
            pdf_file = generate_pdf_from_expenses(expenses)

            # Return the PDF as a response
            response = HttpResponse(pdf_file, content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="expenses_report.pdf"'
            return response

    except ObjectDoesNotExist:
        return HttpResponse('Employee does not exist.', status=400)

    except Exception as e:
        return HttpResponse(f'Error: {str(e)}', status=500)

    return render(request, 'emp_temp/add_expenses.html', {'employee': employee})






from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from PIL import Image as PILImage
from io import BytesIO
from .models import Company, Receipt
from collections import defaultdict

def generate_pdf_from_expenses(expenses):
    company = Company.objects.first() 
    company = Company.objects.first() # Assuming you have a Company model
    buffer = BytesIO()
    pdf = SimpleDocTemplate(buffer, pagesize=landscape(letter), rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=72)
    styles = getSampleStyleSheet()

    # Add custom styles
    styles.add(ParagraphStyle(name='Center', alignment='CENTER'))
    bold_style = styles['Normal']
    bold_style.fontName = 'Helvetica-Bold'  # Set font to bold

    # Define paragraph style for table content with reduced font size
    table_content_style = ParagraphStyle(name='TableContent', fontSize=9)


    current_date = datetime.now().strftime('%d-%m-%Y')

    # Create a paragraph for the date
    date_paragraph = Paragraph(f"Date: {current_date}", styles['Normal'])

    # Create a table to position the date paragraph at the top right corner
    date_table = Table([[date_paragraph]], colWidths=[1.5*inch], hAlign='RIGHT')
    date_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
    ]))

    # List of elements to add to the PDF
    elements = [
        date_table,  
        Paragraph(company.company_name, styles['Title']),
        Paragraph("Travelling Expenses Report", styles['Title']),
        # Paragraph(f"{employee.company.company_name} ", styles['Title']),
        

    ]


    # List of elements to add to the PDF
    # elements = [
    #     Paragraph("Travelling Expenses Report", styles['Title']),
    # ]
    total_amt = sum(expense.food_price + expense.transport_fare + expense.accommodation + expense.other for expense in expenses)
    total_miscellaneous = sum(expense.miscellaneous for expense in expenses)
    total_reimbursement = total_amt + total_miscellaneous
    amount_in_words = convert_to_words(total_reimbursement)
    amount_in_words_para = Paragraph(f"<b>Total Amount in Words:</b> {amount_in_words} only ", bold_style)
    # Dictionary to store unique batches and their data
    batch_data = defaultdict(list)
    batch_receipt_images = set()

    # Collect data and receipts for each expense
    for expense in expenses:
        batch_data[expense.batch_id].append(expense)

    processed_expense_batch_ids = set()  # Track processed expense batch IDs
    for expense in expenses:
        if expense.batch_id not in processed_expense_batch_ids:
            receipts = Receipt.objects.filter(travel_expense=expense)
            for receipt in receipts:
                batch_receipt_images.add(receipt.image.path)
            processed_expense_batch_ids.add(expense.batch_id)

    # Iterate over each batch to generate PDF content
    for batch_id, expenses_in_batch in batch_data.items():
        if expenses_in_batch:
            # Start a new page for each batch
            # elements.append(Paragraph(f"Batch ID: {batch_id}", styles['Title']))

            # Table data for employee information (assuming it's the same for all expenses in the batch)
            employee_info_data = [
                ['Employee Name', 'Employee ID', 'Designation', 'Department'],
                [f"{expenses_in_batch[0].employee.user.first_name} {expenses_in_batch[0].employee.user.last_name}", expenses_in_batch[0].employee.emp_id, expenses_in_batch[0].employee.designation, ]
            ]
            # Create the employee information table (assuming it's the same for all expenses in the batch)
            employee_info_table = Table(employee_info_data, colWidths=[2.5*inch, 2.5*inch, 2.5*inch, 2.5*inch])  # Adjusted widths
            employee_info_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),  # Align all cells to the left
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 7),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ]))
            elements.append(employee_info_table)
            elements.append(Spacer(1, 0.2*inch))

            # Table data for a new table above expenses table
            new_table_data = [
                ['', 'FROM', '','TO','','','','','','','','','']
            ]
            new_table = Table(new_table_data, colWidths=[0.5*inch, 1.7*inch,0.0*inch, 1.7*inch, 0.0*inch, 0.9*inch,
                                                 0.9*inch, 0.9*inch, 0.7*inch, 0.7*inch, 0.6*inch, 0.7*inch, 0.75*inch])   # Adjusted widths
          
            new_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.white),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 7),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ]))
            elements.append(new_table)

            # Table data for expenses
            table_data = [
                [Paragraph("Sr. No", bold_style), Paragraph("From", bold_style), Paragraph("Date", bold_style),
                 Paragraph("To", bold_style), Paragraph("Date", bold_style), Paragraph("Purpose", bold_style),
                 Paragraph("Distance", bold_style), Paragraph("Transport", bold_style), Paragraph("Food", bold_style),
                 Paragraph("Fare", bold_style), Paragraph("Stay", bold_style), Paragraph("Other", bold_style),
                 Paragraph("Total", bold_style)]
            ]

            for idx, expense in enumerate(expenses_in_batch, start=1):
                table_data.append([
                    idx,
                    Paragraph(expense.from_place, table_content_style),
                    Paragraph(expense.from_date.strftime('%d-%m-%Y'), table_content_style),
                    Paragraph(expense.to_place, table_content_style),
                    Paragraph(expense.to_date.strftime('%d-%m-%Y'), table_content_style),
                    Paragraph(expense.purpose, table_content_style),
                    Paragraph(str(expense.distance), table_content_style),
                    Paragraph(expense.model_of_travel, table_content_style),
                    Paragraph(str(expense.food_price), table_content_style),
                    Paragraph(str(expense.transport_fare), table_content_style),
                    Paragraph(str(expense.accommodation), table_content_style),
                    Paragraph(str(expense.other), table_content_style),
                    Paragraph(str(expense.total), table_content_style),
                ])

            # Define table style for expenses
            table_style = TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 7),
                ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('BACKGROUND', (-2, -1), (-1, -1), colors.lightgrey),
                ('TEXTCOLOR', (-2, -1), (-1, -1), colors.white),
                ('FONTNAME', (-2, -1), (-1, -1), 'Helvetica-Bold'),
            ])

            # Create the expense table
            expense_table = Table(table_data, colWidths=[0.5*inch, 0.8*inch, 0.9*inch, 0.8*inch, 0.9*inch, 0.9*inch,
                                                 0.9*inch, 0.9*inch, 0.7*inch, 0.7*inch, 0.6*inch, 0.7*inch, 0.75*inch])  # Adjusted column widths
            expense_table.setStyle(table_style)
            elements.append(expense_table)

            # Table data for additional table below expenses table
            additional_table_data = [
                ['', '', '','','','','','','','','','Total',total_amt]
            ]
            additional_table = Table(additional_table_data, colWidths=[0.5*inch, 0.8*inch, 0.9*inch, 0.8*inch, 0.9*inch, 0.9*inch,
                                                 0.9*inch, 0.9*inch, 0.7*inch, 0.7*inch, 0.6*inch, 0.7*inch, 0.75*inch])
            additional_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.white),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 7),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ]))
            elements.append(additional_table)
            elements.append(Spacer(1, 0.1*inch))

            

            # Table data for another table with a single row
            single_row_table_data = [
                ['', '', '','','','','','','','','Miscellaneous Expense',total_miscellaneous],
                ['', '', '','','','','','','','','Total Reimbursement',total_reimbursement]
            ]
            single_row_table = Table(single_row_table_data, colWidths=[0.5*inch, 0.8*inch, 0.9*inch, 0.8*inch, 0.9*inch, 0.9*inch,
                                                  0.9*inch, 0.8*inch, 0.6*inch, 0.6*inch, 1.55*inch, 0.8*inch])  # Adjusted widths
            single_row_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.white),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 7),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ]))
            elements.append(single_row_table)

            elements.append(Spacer(1, 0.2*inch))
            elements.append(amount_in_words_para)
            elements.append(Spacer(1, 1*inch))
           
            
            
            # "Prepared By" and "Authorized By" section with alignment adjustments
            prepared_by = Paragraph("Prepared By", styles['Normal'])
            prepared_name = Paragraph(f"{expenses[0].employee.user.first_name} {expenses[0].employee.user.last_name}", styles['Normal'])
            authorized_by = Paragraph("Authorized By", styles['Normal'])
            authorized_name = Paragraph(f"{expenses[0].employee.reporting}", styles['Normal'])
            # Table for signatures with alignment, adding an empty column for spacing
            signatures_data = [
                [prepared_by, '', authorized_by],
                [prepared_name, '', authorized_name]
            ]

            # Increase the width of the empty column to add more space between the prepared and authorized sections
            signatures_table = Table(signatures_data, colWidths=[2*inch, 5*inch, 2*inch])

            signatures_table.setStyle(TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ]))

            elements.append(signatures_table)  # Add a small space after the table

    # Add receipt images as standalone elements after processing all batches
    if batch_receipt_images:
        elements.append(PageBreak())  # Start a new page for images
        elements.append(Paragraph("Receipt Images", styles['Title']))
        for receipt_path in batch_receipt_images:
            try:
                pil_image = PILImage.open(receipt_path)

                # Resize the image if it exceeds 2 inches in width or height
                max_dimension = 2 * inch
                if pil_image.width > max_dimension or pil_image.height > max_dimension:
                    pil_image.thumbnail((max_dimension, max_dimension))

                # Convert image to PNG format and add to elements list
                image_buffer = BytesIO()
                pil_image.save(image_buffer, format='PNG')
                image_buffer.seek(0)
                receipt_image = Image(image_buffer, width=2*inch, height=2*inch)  # Adjust size as needed
                elements.append(receipt_image)
                elements.append(Spacer(1, 0.2*inch))  # Add a small space after each image

            except Exception as e:
                print(f"Error loading receipt image: {e}")

    # Build the PDF with the elements
    pdf.build(elements)

    # Get PDF buffer value and close the buffer
    pdf_buffer = buffer.getvalue()
    buffer.close()


    try:
        emp_id = expenses[0].employee.emp_id  # Assuming emp_id is accessible via employee object
        emp_name = f"{expenses[0].employee.user.first_name} {expenses[0].employee.user.last_name}"  # Assuming employee name is accessible via user object
        current_date = now()

        # Create an ExpenseReport instance
        expense_report = ExpenseReport(emp_id=emp_id, emp_name=emp_name, date_created=current_date)
        expense_report.pdf_file.save(f'{emp_id}_expense_report.pdf', ContentFile(pdf_buffer))
        expense_report.save()

        return pdf_buffer

    except Exception as e:
        print(f"Error saving PDF to database: {e}")
        return None















from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.hashers import make_password
from .models import Employee


# def employee_update(request, emp_id):
#     employee = Employee.objects.get(emp_id=emp_id)
#     if request.method == 'POST':
#         form = EmployeeUpdateForm(request.POST, request.FILES, instance=employee)
#         if form.is_valid():

#             if 'password' in form.cleaned_data:
#                 new_password = form.cleaned_data['password']
#                 if new_password:
#                     user = employee.user
#                     user.password = make_password(new_password)
#                     user.save()
#             form.save()
#             employee.save()
#             employee.user.save()
#             return redirect('employee_update', emp_id=emp_id)  # Redirect to employee detail page
#     else:
#         form = EmployeeUpdateForm(instance=employee)
#     return render(request, 'hr_temp/employee_update.html', {'form': form})

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from datetime import timedelta
from .models import Employee

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from .models import Employee
from datetime import timedelta

def employee_update(request, emp_id):
    employee = get_object_or_404(Employee, emp_id=emp_id)
    user = employee.user  # Get the associated user instance
    
    if request.method == 'POST':
        # Update user data including password if necessary
        if request.POST.get('username'):
            user.username = request.POST.get('username')
        if request.POST.get('first_name'):
            user.first_name = request.POST.get('first_name')
        if request.POST.get('last_name'):
            user.last_name = request.POST.get('last_name')
        if request.POST.get('email'):
            user.email = request.POST.get('email')
        if request.POST.get('password'):
            user.set_password(request.POST.get('password'))  # Set password securely
        user.save()
        
        # Update employee data
        if request.POST.get('reporting'):
            employee.reporting = request.POST.get('reporting')
        if request.POST.get('bank'):
            employee.bank = request.POST.get('bank')
        if request.POST.get('email2'):
            employee.email2 = request.POST.get('email2')
        if request.POST.get('emp_id'):
            employee.emp_id = request.POST.get('emp_id')
        
        if request.POST.get('title'):
            employee.title = request.POST.get('title')
        
        
        if request.POST.get('mobile_no'):
            employee.mobile_no = int(request.POST.get('mobile_no'))
        if request.POST.get('emg_mobile_no_1'):
            employee.emg_mobile_no_1 = int(request.POST.get('emg_mobile_no_1'))
        if request.POST.get('emg_mobile_no_2'):
            employee.emg_mobile_no_2 = int(request.POST.get('emg_mobile_no_2'))
        if request.POST.get('emg_relation_1'):
            employee.emg_relation_1 = request.POST.get('emg_relation_1')
        if request.POST.get('emg_relation_2'):
            employee.emg_relation_2 = request.POST.get('emg_relation_2')
        if request.POST.get('pan_no'):
            employee.pan_no = request.POST.get('pan_no')
        if request.POST.get('aadhaar'):
            employee.aadhaar = int(request.POST.get('aadhaar'))
        if request.POST.get('designation'):
            employee.designation = request.POST.get('designation')
        if request.POST.get('company_id'):
            employee.company_id = int(request.POST.get('company_id'))
        if request.POST.get('address'):
            employee.address = request.POST.get('address')
        if request.POST.get('current_address'):
            employee.current_address = request.POST.get('current_address')
        if request.POST.get('salary'):
            employee.salary = int(request.POST.get('salary'))
        if request.POST.get('standard_basic'):
            employee.standard_basic = int(request.POST.get('standard_basic'))
        if request.POST.get('standard_HRA'):
            employee.standard_HRA = int(request.POST.get('standard_HRA'))
        if request.POST.get('standard_edu_allowance'):
            employee.standard_edu_allowance = int(request.POST.get('standard_edu_allowance'))
        if request.POST.get('standard_statutory_bonus'):
            employee.standard_statutory_bonus = int(request.POST.get('standard_statutory_bonus'))
        if request.POST.get('standard_conveyance_allowance'):
            employee.standard_conveyance_allowance = int(request.POST.get('standard_conveyance_allowance'))
        if request.POST.get('standard_LTA'):
            employee.standard_LTA = int(request.POST.get('standard_LTA'))
        if 'other_allowance' in request.POST:
            other_allowance_value = request.POST['other_allowance']
            employee.other_allowance = int(other_allowance_value) if other_allowance_value.strip() else None

        if request.FILES.get('aadhar_image'):
            employee.aadhar_image = request.FILES.get('aadhar_image')
        if request.FILES.get('pancard_image'):
            employee.pancard_image = request.FILES.get('pancard_image')
        if request.POST.get('bank_account_no'):
            employee.bank_account_no = int(request.POST.get('bank_account_no'))
        if request.POST.get('ifsc_code'):
            employee.ifsc_code = request.POST.get('ifsc_code')
        if request.POST.get('blood_group'):
            employee.blood_group = request.POST.get('blood_group')
        if request.POST.get('gender'):
            employee.gender = request.POST.get('gender')
        if request.POST.get('marital_status'):
            employee.marital_status = request.POST.get('marital_status')
        if request.POST.get('anniversary_date'):
            employee.anniversary_date = request.POST.get('anniversary_date')
        if request.POST.get('date_of_birth'):
            employee.date_of_birth = request.POST.get('date_of_birth')
        if request.POST.get('date_of_joining'):
            employee.date_of_joining = request.POST.get('date_of_joining')
        if request.POST.get('date_of_probation'):
            employee.date_of_probation = request.POST.get('date_of_probation')
        if request.POST.get('profile_picture'):
            employee.profile_picture = request.FILES.get('profile_picture')
        if request.POST.get('annual_ctc'):
            employee.annual_ctc = int(request.POST.get('annual_ctc'))
        if request.POST.get('nominee'):
            employee.nominee = request.POST.get('nominee')
        if request.POST.get('nominee_relation'):
            employee.nominee_relation = request.POST.get('nominee_relation')
        if request.POST.get('CL'):
            employee.CL = int(request.POST.get('CL'))
        if request.POST.get('SL'):
            employee.SL = int(request.POST.get('SL'))
        if request.POST.get('PL'):
            employee.PL = int(request.POST.get('PL'))
        if request.POST.get('UL'):
            employee.UL = int(request.POST.get('UL'))
        if request.POST.get('wfh_count'):
            employee.wfh_count = int(request.POST.get('wfh_count'))
        if request.POST.get('od_count'):
            employee.od_count = int(request.POST.get('od_count'))
        
        employee.save()
        
        return redirect('employee_update', emp_id=employee.emp_id)  # Replace with your employee detail URL name
    
    return render(request, 'hr_temp/employee_update.html', {'employee': employee})





from django.core.paginator import Paginator
@login_required
def view_expenses(request):
    expense_reports = ExpenseReport.objects.all().order_by('-date_created')  # Reverse order to show latest first

    paginator = Paginator(expense_reports, 10)  # Show 10 reports per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'expense_reports': page_obj,
    }
    return render(request, 'hr_temp/view_expenses.html', context)



from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image
from reportlab.lib.enums import TA_CENTER
from io import BytesIO
from PIL import Image as PILImage

def convert_to_words(num):
    num = int(num)  # Ensure num is an integer
    
    if num == 0:
        return "zero"
    
    ones = ["", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine"]
    tens = ["", "", "Twenty", "Thirty", "Forty", "Fifty", "Sixty", "Seventy", "Eighty", "Ninety"]
    teens = ["Ten", "Eleven", "Twelve", "Thirteen", "Fourteen", "Fifteen", "Sixteen", "Seventeen", "Eighteen", "Nineteen"]
    
    def get_words(n, suffix):
        if n == 0:
            return ""
        elif n < 10:
            return ones[n] + suffix
        elif n < 20:
            return teens[n - 10] + suffix
        elif n < 100:
            return tens[n // 10] + (ones[n % 10] and " " + ones[n % 10] or "") + suffix
        else:
            return ones[n // 100] + " hundred " + get_words(n % 100, "") + suffix

    crore = num // 10000000
    lakh = (num // 100000) % 100
    thousand = (num // 1000) % 100
    hundred = (num // 100) % 10
    rest = num % 100

    result = ""
    if crore > 0:
        result += get_words(crore, " crore ")
    if lakh > 0:
        result += get_words(lakh, " lakh ")
    if thousand > 0:
        result += get_words(thousand, " thousand ")
    if hundred > 0:
        result += get_words(hundred, " hundred ")
    if rest > 0:
        if num > 100:
            result += "and "
        result += get_words(rest, "")
    
    return result.strip()




def convert_number_to_words(number):
    # Dummy implementation of number to words converter
    words = {1: 'one', 2: 'two', 3: 'three', 4: 'four', 5: 'five', 6: 'six', 7: 'seven', 8: 'eight', 9: 'nine', 0: 'zero'}
    return ' '.join(words[int(digit)] for digit in str(number))



def add_page_number(canvas, doc):
    page_num = canvas.getPageNumber()
    text = f"Page {page_num}"
    canvas.drawRightString(7.87402 * inch, 0.787402 * inch, text)





def admin_required(view_func):
    """
    Decorator for views that checks whether the user is an admin.
    """
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_superuser:
            raise PermissionDenied
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def employee_required(view_func):
    """
    Decorator for views that checks whether the user is an employee.
    """
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_superuser:
            raise PermissionDenied
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def handle_permission_denied(request, exception):
    """
    Custom handler for PermissionDenied exception.
    """
    return render(request, 'permission_denied.html', status=403)

def dashboard_view(request):
    employee = get_object_or_404(Employee, user=request.user)
    context = {
        'employee': employee
    }
    return render(request, 'emp_temp/sidebar_template.html', context)


@login_required
def add_holiday(request):
    if request.method == "POST":
        form = HolidayForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('holiday_list')  # Redirect to a list of holidays or another appropriate page
    else:
        form = HolidayForm()
    return render(request, 'hr_temp/add_holiday.html', {'form': form})

@login_required
def holiday_list(request):
    holidays = Holiday.objects.all()
    return render(request, 'hr_temp/holiday_list.html', {'holidays': holidays})



def get_notifications(request):
    current_time = datetime.now().time()
    today_attendances = Attendance.objects.filter(date=datetime.now().date())

    notifications = []

    for attendance in today_attendances:
        if attendance.intime is not None:
            notification = {
                'employee': (attendance.employee.user.first_name)+(attendance.employee.user.last_name),  # Accessing employee's first name
                'intime': attendance.intime.strftime("%H:%M"),
                'outtime': None,
                'message': f'{attendance.employee.user.first_name} {attendance.employee.user.last_name} has arrived at {attendance.intime.strftime("%H:%M")}',
                'timestamp': datetime.now().strftime("%Y-%m-%d")
            }
            notifications.append(notification)

        if attendance.intime is not None and attendance.outtime is not None and attendance.intime <= current_time:
            notification = {
                'employee': attendance.employee.user.first_name,  # Accessing employee's first name
                'intime': attendance.intime.strftime("%H:%M"),
                'outtime': attendance.outtime.strftime("%H:%M"),
                'message': f'Employee {attendance.employee.first_name} has left at {attendance.outtime.strftime("%H:%M")}',
                'timestamp': datetime.now().strftime("%Y-%m-%d")
            }
            notifications.append(notification)

    return JsonResponse(notifications, safe=False)


@login_required
def emp_info(request):
    # Get the currently logged-in user
    user = request.user
    
    
    # Retrieve the associated employee object
    try:
        employee = Employee.objects.get(user=user)
    except Employee.DoesNotExist:
        # Handle the case where no employee is found for the logged-in user
        # Redirect to an appropriate page or display an error message
        return HttpResponse("Employee data not found.")
    
    if request.method == 'POST':


        try:
        # Retrieve data from request.POST
            emp_id = request.POST.get('emp_id')
            email = request.POST.get('email')
            title = request.POST.get('title')
            reporting  = request.Post.get('reporting')
            first_name = request.POST.get('first_name')
            midde_name = request.POST.get('middle_name')
            last_name = request.POST.get('last_name')
            mobile_no = request.POST.get('mobile_no')
            emg_mobile_no_1 = request.POST.get('emg_mobile_no_1')
            emg_mobile_no_2 = request.POST.get('emg_mobile_no_2')
            emg_relation_1 = request.POST.get('emg_relation_1')
            emg_relation_2 = request.POST.get('emg_relation_2')
            pan_no = request.POST.get('pan_no')
            aadhaar = request.POST.get('aadhaar')
            designation = request.POST.get('designation')
            address = request.POST.get('address')
            current_address = request.POST.get('current_address')
            salary = request.POST.get('salary')
            bank_account_no = request.POST.get('bank_account_no')
            ifsc_code = request.POST.get('ifsc_code')
            blood_group = request.POST.get('blood_group')
            gender = request.POST.get('gender')
            nominee = request.POST.get('nominee')
            nominee_relation = request.POST.get('nominee_relation')
            date_of_birth = request.POST.get('date_of_birth')
            date_of_joining = request.POST.get('date_of_joining')
            date_of_probation = request.POST.get('date_of_probation')
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')
            marital_status = request.POST.get('marital_status')
            profile_picture = request.FILES.get('profile_picture')
            aadhar_image = request.FILES.get('aadhar_image')
            pancard_image = request.FILES.get('pan_image')
            # Retrieve the existing employee object

            if profile_picture:
                file_name = default_storage.save('media/images/' + profile_picture.name, ContentFile(profile_picture.read()))
                profile_picture =  file_name
            # Save profile_picture_path in your Employee model
            
        # Handle Aadhaar image upload
            if aadhar_image:
                file_name = default_storage.save('media/images/' + aadhar_image.name, ContentFile(aadhar_image.read()))
                aadhar_image =  file_name
            # Save aadhar_image_path in your Employee model
            
        # Handle PAN image upload
            if pancard_image:
                file_name = default_storage.save('media/images/' + pancard_image.name, ContentFile(pancard_image.read()))
                pancard_image =  file_name
            try:
                employee = Employee.objects.get(emp_id=emp_id)
            except Employee.DoesNotExist:
                # Handle the case where no employee is found for the given ID
                return HttpResponse("Employee not found.")
            
            # Update the fields if they are provided in the form
            if email:
                employee.email = email
            if first_name:
                employee.user.first_name = first_name
            if last_name:
                employee.user.last_name = last_name
            if mobile_no:
                employee.mobile_no = mobile_no
            if emg_mobile_no_1:
                employee.emg_mobile_no_1 = emg_mobile_no_1
            if emg_mobile_no_2:
                employee.emg_mobile_no_2 = emg_mobile_no_2
            if emg_relation_1:
                employee.emg_relation_1 = emg_relation_1
            if emg_relation_2:
                employee.emg_relation_2 = emg_relation_2
            if pan_no:
                employee.pan_no = pan_no
            if aadhaar:
                employee.aadhaar = aadhaar
            if designation:
                employee.designation = designation
            if address:
                employee.address = address
            if current_address:
                employee.current_address = current_address
            if salary:
                employee.salary = salary
            if bank_account_no:
                employee.bank_account_no = bank_account_no
            if ifsc_code:
                employee.ifsc_code = ifsc_code
            if blood_group:
                employee.blood_group = blood_group
            if gender:
                employee.gender = gender
            if date_of_birth:
                employee.date_of_birth = date_of_birth
            if date_of_joining:
                employee.date_of_joining = date_of_joining
            if date_of_probation:
                employee.date_of_probation = date_of_probation
            if reporting:
                employee.reporting = reporting
                
            
            
            if new_password and new_password == confirm_password:
                # Hash the new password securely
                hashed_password = make_password(new_password)
                # Set the new hashed password for the user
                employee.user.password = hashed_password
                # Save the user to update the password
                employee.user.save()
                # Update the session auth hash to prevent the user from being logged out
                update_session_auth_hash(request, employee.user)
            
            
            # Save the changes
            employee.save()
            employee.user.save()
            messages.success(request, 'Employee information updated successfully.')
            # Redirect to the appropriate page after form submission
            return redirect('emp_info')  # Replace 'emp_dashboard' with the URL name of the dashboard page
    
        except Exception as e:
                # Add warning message
                messages.warning(request, f'Warning: Some information could not be updated. {str(e)}')
                # Redirect back to the same page
                return redirect('emp_info')
    
            

    # Render the template and pass the employee object to the template context
    return render(request, 'emp_temp/emp_info.html', {'employee': employee})

@login_required
def leave_request_list(request):
    leave_requests = LeaveRequest.objects.all()
    return render(request, 'hr_temp/leave_request_list.html', {'leave_requests': leave_requests})

@login_required
def leave_request_detail(request, pk,status=None):
    leave_request = LeaveRequest.objects.get(pk=pk)
    form = LeaveRequestApprovalForm(instance=leave_request)

    # Check if the leave request is approved or rejected
    success_message = None
    rejected_message = None
    if leave_request.status == 'approved':
        success_message = 'Leave request has been approved.'
    elif leave_request.status == 'rejected':
        rejected_message = 'Leave request has been rejected.'

    return render(request, 'hr_temp/leave_request_detail.html', {'leave_request': leave_request, 'form': form, 'success_message': success_message, 'rejected_message': rejected_message})





@login_required
def approve_leave_request(request, pk):
    leave_request = LeaveRequest.objects.get(pk=pk)
    if request.method == 'POST':
        form = LeaveRequestApprovalForm(request.POST, instance=leave_request)
        if form.is_valid():
            leave_request = form.save()
            if leave_request.status == 'approved':
                # Deduct leave days from employee's leave balance
                employee = leave_request.employee
                leave_type = leave_request.leave_type
                days_requested = leave_request.days_requested
                employee.deduct_leave(leave_type, days_requested)

                # Add success message for approval
                messages.success(request, 'Leave request has been approved.')

                # Redirect to leave_request_detail view with status parameter
                return redirect('leave_request_detail', pk=pk, status='approved')
            elif leave_request.status == 'rejected':
                # Add success message for rejection
                messages.success(request, 'Leave request has been rejected.')

                # Redirect to leave_request_detail view with status parameter
                return redirect('leave_request_detail', pk=pk, status='rejected')
    else:
        form = LeaveRequestApprovalForm(instance=leave_request)
    return render(request, 'hr_temp/leave_request_approve.html', {'form': form})


def leave_request_reject(request, pk):
    """
    View to reject a leave request.
    """
    leave_request = get_object_or_404(LeaveRequest, pk=pk)
    leave_request.reject()
    messages.success(request, 'Leave request rejected successfully!')
    return redirect('leave_request_list')


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if user.is_superuser:
                    # Redirect superuser to admin panel or any superuser-specific page
                    return redirect('dashboard')
                else:
                    # Redirect regular user to their dashboard or any user-specific page
                    return redirect('emp_dashboard')
            else:
                # Invalid login
                return render(request, 'login.html', {'form': form, 'error_message': 'Invalid username or password.'})
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form, 'error_message': ''})


from django.contrib.auth import logout
from django.shortcuts import redirect
from django.urls import reverse
from django.core.cache import cache

from django.contrib.auth import logout
from django.shortcuts import redirect
from django.urls import reverse
from django.core.cache import cache

def user_logout(request):
    # Clear the session
    request.session.flush()
    # Clear the cache associated with the user (replace 'user_id' with the actual user identifier)
    cache_key = f'user_{request.user.id}_cache_key'
    cache.delete(cache_key)
    # Redirect to the login page
    return redirect(reverse('login'))

from django.db import connection
from .models import TravelExpense
from django.db.models import Sum
from datetime import date
from django.utils.timezone import now
from django.db.models import Sum , F, Value,DecimalField
from django.db.models.functions import Coalesce, Cast
from decimal import Decimal
from django.db.models import Q
# @login_required
# @admin_required
# def dashboard(request):
#     today = now().date()
#     current_month = today.month
#     current_year = today.year
    

#     # Fetch all companies for the dropdown
#     companies = Company.objects.all()
#     holidays = Holiday.objects.all()

#     selected_company_name = request.GET.get('company_name', None)

#     if selected_company_name:
#         # Fetch company details based on selected company name
#         company = get_object_or_404(Company, company_name=selected_company_name)

#         # Employee statistics for the selected company
#         employees = Employee.objects.filter(company=company)
#         total_employees = employees.count()
        
#         on_leave_today = LeaveRequest.objects.filter(employee__company=company, date=today, status='approved').count()
#         wfh_today = Attendance.objects.filter(employee__company=company, date=today, wfhstatus='WFH').count()

#         employees_on_leave = LeaveRequest.objects.filter(employee__company=company, date=today, status='approved').select_related('employee')
#         employees_on_wfh = Attendance.objects.filter(employee__company=company, date=today, wfhstatus='WFH').select_related('employee')
#         current_month_attendance = Attendance.objects.filter(employee__company=company, date__month=current_month, date__year=current_year)
        
#         # Filter expenses by company
#         expenses = TravelExpense.objects.filter(employee__company=company)
#         employees_present_count = Attendance.objects.filter(
#             Q(date=today, intime__isnull=False) | Q(date=today, wfhstatus='WFH'),
#             employee__company=company
#         ).count()  
#     else:
#         # Overall statistics without filtering by company
#         employees = Employee.objects.all()
#         total_employees = employees.count()
#         on_leave_today = LeaveRequest.objects.filter(date=today, status='approved').count()
#         wfh_today = Attendance.objects.filter(date=today, wfhstatus='WFH').count()
        
#         employees_on_leave = LeaveRequest.objects.filter(date=today, status='approved').select_related('employee')
#         employees_on_wfh = Attendance.objects.filter(date=today, wfhstatus='WFH').select_related('employee')
#         current_month_attendance = Attendance.objects.filter(date__month=current_month, date__year=current_year)
#         employees_present_count = Attendance.objects.filter(
#             Q(date=today, intime__isnull=False) | Q(date=today, wfhstatus='WFH')
#         ).count()
            

#         # Fetch all expenses if no company is selected
#         expenses = TravelExpense.objects.all()

#     # Calculate total reimbursement
#     total_amt = sum(expense.food_price + expense.transport_fare + expense.accommodation + expense.other for expense in expenses)
#     total_miscellaneous = sum(expense.miscellaneous for expense in expenses)
#     total_reimbursement = total_amt + total_miscellaneous
    

#     # Calculate total reimbursement per employee
#     expenses_by_employee = expenses.values(
#         'employee__id', 'employee__user__first_name', 'employee__user__last_name'
#     ).annotate(
#         total_reimbursement=Coalesce(
#             Cast(Sum(
#                 F('food_price') + F('transport_fare') + F('accommodation') + F('other') + F('miscellaneous')
#             ), output_field=DecimalField()),
#             Value(Decimal('0'))
#         )
#     )

#     total_present_employees = total_employees - on_leave_today
#     total_working_days = current_month_attendance.count()
#     late_entries = current_month_attendance.filter(lateintime__isnull=False).count()
#     early_exits = current_month_attendance.filter(earlygoingtime__isnull=False).count()
    
#     recent_leave_requests = LeaveRequest.objects.filter(employee__in=employees, status='approved').order_by('-created_at')[:5]
#     upcoming_birthdays = employees.filter(date_of_birth__month=current_month)
#     upcoming_anniversaries = employees.filter(date_of_joining__month=current_month)
#     upcoming_wed_anniversary = employees.filter(anniversary_date__month = current_month)

#     context = {
#         'companies': companies,
#         'selected_company_name': selected_company_name,
#         'total_employees': total_employees,
#         'on_leave_today': on_leave_today,
#         'total_present_employees': total_present_employees,
#         'wfh_today': wfh_today,
#         'recent_leave_requests': recent_leave_requests,
#         'total_working_days': total_working_days,
#         'late_entries': late_entries,
#         'early_exits': early_exits,
#         'upcoming_birthdays': upcoming_birthdays,
#         'upcoming_anniversaries': upcoming_anniversaries,
#         'upcoming_wed_anniversary': upcoming_wed_anniversary,
#         'holidays': holidays,
#         'employees_present_count': employees_present_count,
        
#         # 'total_reimbursement': total_reimbursement,
#         # 'expenses_by_employee': expenses_by_employee,
#         'employees_on_leave': [leave.employee for leave in employees_on_leave],
#         'employees_on_wfh': [attendance.employee for attendance in employees_on_wfh],
#     }

#     return render(request, 'hr_temp/hr_dashboard.html', context)
@login_required
@admin_required
def dashboard(request):
    today = now().date()
    current_month = today.month
    current_year = today.year

    # Fetch all companies for the dropdown
    companies = Company.objects.all()
    holidays = Holiday.objects.all()

    selected_company_name = request.GET.get('company_name', None)

    if selected_company_name:
        # Fetch company details based on selected company name
        company = get_object_or_404(Company, company_name=selected_company_name)

        # Employee statistics for the selected company
        employees = Employee.objects.filter(company=company)
        total_employees = employees.count()
        on_leave_today = LeaveRequest.objects.filter(employee__company=company, date=today, status='approved').count()
        wfh_today = Attendance.objects.filter(employee__company=company, date=today, wfhstatus='WFH').count()

        employees_on_leave = LeaveRequest.objects.filter(employee__company=company, date=today, status='approved').select_related('employee')
        employees_on_wfh = Attendance.objects.filter(employee__company=company, date=today, wfhstatus='WFH').select_related('employee')
        current_month_attendance = Attendance.objects.filter(employee__company=company, date__month=current_month, date__year=current_year)
        employees_present_count = Attendance.objects.filter(
            Q(date=today, intime__isnull=False) | Q(date=today, wfhstatus='WFH'),
            employee__company=company
        ).count()
       
        # Filter expenses by company
        expenses = TravelExpense.objects.filter(employee__company=company)
    else:
        # Overall statistics without filtering by company
        employees = Employee.objects.all()
        total_employees = employees.count()
        on_leave_today = LeaveRequest.objects.filter(date=today, status='approved').count()
        wfh_today = Attendance.objects.filter(date=today, wfhstatus='WFH').count()

        employees_on_leave = LeaveRequest.objects.filter(date=today, status='approved').select_related('employee')
        employees_on_wfh = Attendance.objects.filter(date=today, wfhstatus='WFH').select_related('employee')
        current_month_attendance = Attendance.objects.filter(date__month=current_month, date__year=current_year)
        employees_present_count = Attendance.objects.filter(
            Q(date=today, intime__isnull=False) | Q(date=today, wfhstatus='WFH')
        ).count()

        # Fetch all expenses if no company is selected
        expenses = TravelExpense.objects.all()

    # Calculate total reimbursement
    total_amt = sum(expense.food_price + expense.transport_fare + expense.accommodation + expense.other for expense in expenses)
    total_miscellaneous = sum(expense.miscellaneous for expense in expenses)
    total_reimbursement = total_amt + total_miscellaneous

    # Calculate total reimbursement per employee
    expenses_by_employee = expenses.values(
        'employee__id', 'employee__user__first_name', 'employee__user__last_name'
    ).annotate(
        total_reimbursement=Coalesce(
            Cast(Sum(
                F('food_price') + F('transport_fare') + F('accommodation') + F('other') + F('miscellaneous')
            ), output_field=DecimalField()),
            Value(Decimal('0'))
        )
    )

    total_present_employees = total_employees - on_leave_today
    total_working_days = current_month_attendance.count()
    late_entries = current_month_attendance.filter(lateintime__isnull=False).count()
    early_exits = current_month_attendance.filter(earlygoingtime__isnull=False).count()
   
    recent_leave_requests = LeaveRequest.objects.filter(employee__in=employees, status='approved').order_by('-created_at')[:5]
   
    # Filter upcoming birthdays
    upcoming_birthdays = employees.filter(
        date_of_birth__month=current_month,
        date_of_birth__day__gte=today.day
    ).order_by('date_of_birth__day')

    # Filter upcoming work anniversaries
    upcoming_anniversaries = employees.filter(
        date_of_joining__month=current_month,
        date_of_joining__day__gte=today.day
    ).order_by('date_of_joining__day')

    # Filter upcoming wedding anniversaries
    upcoming_wed_anniversary = employees.filter(
        anniversary_date__month=current_month,
        anniversary_date__day__gte=today.day
    ).order_by('anniversary_date__day')


    context = {
        'companies': companies,
        'selected_company_name': selected_company_name,
        'total_employees': total_employees,
        'on_leave_today': on_leave_today,
        'total_present_employees': total_present_employees,
        'wfh_today': wfh_today,
        'recent_leave_requests': recent_leave_requests,
        'total_working_days': total_working_days,
        'late_entries': late_entries,
        'early_exits': early_exits,
        'upcoming_birthdays': upcoming_birthdays,
        'upcoming_anniversaries': upcoming_anniversaries,
        'upcoming_wed_anniversary': upcoming_wed_anniversary,
        'holidays': holidays,
        'employees_present_count': employees_present_count,
        # 'total_reimbursement': total_reimbursement,
        # 'expenses_by_employee': expenses_by_employee,
        'employees_on_leave': [leave.employee for leave in employees_on_leave],
        'employees_on_wfh': [attendance.employee for attendance in employees_on_wfh],
    }

    return render(request, 'hr_temp/hr_dashboard.html', context)


@login_required
def add_company(request):
    """
    View function to handle the addition of a new company.
    Only accessible to authenticated users.
    """
    if request.method == 'POST':
        form = CompanyForm(request.POST, request.FILES)  # Include request.FILES
        if form.is_valid():
            form.save()
            messages.success(request, 'Company details created successfully.')
            return redirect('add_company')  # Redirect to the 'add_company' page or update to the desired URL
    else:
        form = CompanyForm()
    
    return render(request, 'hr_temp/add_company.html', {'form': form})
from datetime import datetime


@login_required
def wfhod_form(request):
    employees = Employee.objects.all()
    
    if request.method == 'POST':
        form = WFHODForm(request.POST)
        if form.is_valid():
            # Process the form data
            date = form.cleaned_data['date']
            
            # Check if the date is in the past
            if date < datetime.now().date():
                messages.error(request, 'Cannot submit data for past dates.')
                return render(request, 'hr_temp/WFHODForm.html', {'form': form, 'employees': employees})

            employee_id = form.cleaned_data['employee']
            wfhstatus = form.cleaned_data['wfhstatus']
            wfhodremark = form.cleaned_data['wfhodremark']
            
            # Create a new Attendance object
            attendance = Attendance(employee_id=employee_id.id, date=date, wfhstatus=wfhstatus, wfhodremark=wfhodremark)
            
            # Save the Attendance object
            attendance.save()

            # Update WFH or OD count for the employee
            employee = attendance.employee
            if attendance.wfhstatus == 'WFH':
                employee.wfh_count += 1
            elif attendance.wfhstatus == 'OD':
                employee.od_count += 1
            employee.save()

            messages.success(request, 'WFH/OD form submitted successfully.')  # Display success message
            return redirect('WFHODForm')  # Redirect to success page upon successful submission
    else:
        form = WFHODForm()
    return render(request, 'hr_temp/WFHODForm.html', {'form': form, 'employees': employees})


from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from django.http import HttpResponse
import io
from datetime import datetime
import calendar
from django.shortcuts import render, redirect
from .models import Employee, SalarySlip, Attendance, LeaveRequest
from django.core.files.base import ContentFile
from django.contrib import messages





















@login_required
def company_list(request):
    companies = Company.objects.all()
    return render(request, 'hr_temp/company_list.html', {'companies': companies})

@login_required
def add_emp(request):
    if request.method == 'POST':
        form = EmployeeCreationForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                employee, user = form.save()
                if employee and user:
                    return JsonResponse({'success': True, 'message': 'Employee added successfully.'})
                else:
                    return JsonResponse({'success': False, 'message': 'Employee Already Exists'})
            except Exception as e:
                return JsonResponse({'success': False, 'message': f'Error saving employee: {str(e)}'})
        else:
            errors = form.errors.as_json()
            return JsonResponse({'success': False, 'message': 'Form submission error.', 'errors': errors}, status=400)
    else:
        form = EmployeeCreationForm()
    return render(request, 'hr_temp/add_emp.html', {'form': form})



def logout(request):
    return render(request, 'login.html')





def emp_dashboard(request):
    today = datetime.now().date()
    outtime_update_form = None
    attendances = None
    user = request.user
    employee = Employee.objects.get(user=user)
    holidays = Holiday.objects.all()
    birthday_message = None
    anniversary_message = None
    birthday_employees = []
    
    
    if request.method == 'POST':
        if 'intime' in request.POST and 'outtime' not in request.POST:
            # If only intime is posted, display the out time update form
            outtime_update_form = OutTimeUpdateForm()
    else:
        # Fetch the latest attendance record for the logged-in user
        latest_attendance = Attendance.objects.filter(employee=employee).order_by('-date').first()
        if latest_attendance and latest_attendance.wfhstatus in ['WFH', 'OD']:
            # If the latest attendance record indicates WFH or OD, don't show the out time update form
            outtime_update_form = None

        # Check if it's the employee's birthday
        if employee.date_of_birth is not None:
            if employee.date_of_birth.month == today.month and employee.date_of_birth.day == today.day:
                birthday_message = "Happy Birthday, {}!".format(employee.user.get_full_name())
                # Your logic to handle the birthday message here
            else:
                # Handle the case where date_of_birth is None
                birthday_message = None 
        

        if employee.anniversary_date:
            if employee.anniversary_date.month == today.month and employee.anniversary_date.day == today.day:
                anniversary_message = "Happy 1st Work Anniversary, {}!".format(employee.user.get_full_name())
            else:
                # Handle the case where anniversary is None
                anniversary_message = None
            
    # Retrieve all attendance records for the logged-in user
    attendances = Attendance.objects.filter(employee=employee).order_by('-date')
    birthday_employees = Employee.objects.filter(date_of_birth__month=today.month, date_of_birth__day=today.day).exclude(emp_id=employee.emp_id)

    return render(request, 'emp_temp/emp_dashboard.html', {
        'outtime_update_form': outtime_update_form,
        'attendances': attendances,
        'employee': employee,
        'birthday_message': birthday_message,
        'holidays':holidays,
        'anniversary_message':anniversary_message,
        'birthday_employees': birthday_employees,
    })



def update_outtime(request, attendance_id):
    attendance = Attendance.objects.get(pk=attendance_id)

    if request.method == 'POST':
        form = OutTimeUpdateForm(request.POST, instance=attendance)  # Pass instance here
        if form.is_valid():
            form.save()
            return redirect('emp_dashboard')
    else:
        form = OutTimeUpdateForm(instance=attendance)  # Pass instance here

    return render(request, 'emp_temp/update_outtime.html',  {'form': form, 'attendance': attendance})

def calculate_late_early(intime, outtime, employee):
    cintime = employee.cintime
    couttime = employee.couttime
    
    # Check if intime and outtime are provided
    if intime and outtime:
        # Calculate late in time
        lateinmin = max(0, (intime.hour * 60 + intime.minute) - (cintime.hour * 60 + cintime.minute))
        
        # Calculate late going if outtime is later than company out time
        if outtime > couttime:
            lategoingmin = max(0, (outtime.hour * 60 + outtime.minute) - (couttime.hour * 60 + couttime.minute))
            earlygoingmin = None
        else:
            earlygoingmin = max(0, (couttime.hour * 60 + couttime.minute) - (outtime.hour * 60 + outtime.minute))
            lategoingmin = None

    else:
        lateinmin = None
        earlygoingmin = None
        lategoingmin = None
        
    if lateinmin is not None:
        lateinmin = "{:02}:{:02}".format(*divmod(lateinmin, 60))
    if earlygoingmin is not None:
        earlygoingmin = "{:02}:{:02}".format(*divmod(earlygoingmin, 60))
    if lategoingmin is not None:
        lategoingmin = "{:02}:{:02}".format(*divmod(lategoingmin, 60))

    return lateinmin, earlygoingmin, lategoingmin





from django.utils import timezone
from django import forms
import logging
logger = logging.getLogger(__name__)

# def emp_attend(request):
#     user = request.user
#     employee = Employee.objects.get(user=user)

#     if request.method == 'POST':
#         form = AttendanceForm(request.POST, initial={'request': request})
#         if form.is_valid():
#             intime = form.cleaned_data['intime']
#             outtime = form.cleaned_data['outtime']
#             date = form.cleaned_data['date']

#             # Check if the date is in the past
#             if date < timezone.now().date():
#                 return HttpResponse("Attendance cannot be recorded for past dates.")

#             # Check if the date is in the future
#             if date > timezone.now().date():
#                 return HttpResponse("Attendance cannot be recorded for future dates.")

#             # Check if there is an approved leave request for the same date
#             leave_request = LeaveRequest.objects.filter(employee=request.user.employee, date=date, status='approved').first()
#             if leave_request:
#                 return HttpResponse("Attendance cannot be recorded because a leave request for this date is already approved.")

#             # Check if attendance already exists for the same date
#             if Attendance.objects.filter(employee=request.user.employee, date=date).exists():
#                 return HttpResponse("Attendance for this date already exists.")

#             company_logic = request.user.employee.company.company_logic

#             # Get the weekday of the attendance date (0=Monday, 5=Saturday, 6=Sunday)
#             weekday = date.weekday()

#             # Check if the attendance date is valid based on company logic
#             if company_logic == 'logic1' and weekday >= 5:
#                 messages.error(request, "Attendance cannot be recorded on weekends for this company.")
#                 return redirect('emp_attend')

#             # Calculate late in time, early going time, and late going time
#             late_in_time, early_going_time, late_going_time = calculate_late_early(intime, outtime, request.user.employee)

#             attendance = form.save(commit=False)
#             attendance.employee = request.user.employee
#             attendance.lateintime = late_in_time  
#             attendance.earlygoingtime = early_going_time
#             attendance.lategointtime = late_going_time
#             attendance.save()

#             messages.success(request, 'Attendance recorded successfully!')
#             logger.info(f"Attendance recorded by IP: {form.get_client_ip()}")

#             return redirect('emp_attend')
#         else:
#             messages.error(request, 'Error submitting attendance. Please check the form.')
#     else:
#         form = AttendanceForm(initial={'request': request})

#     # Initialize outtime_update_form to None by default
#     outtime_update_form = None

#     # Check if intime is posted and no outtime is available
#     if 'intime' in request.POST and 'outtime' not in request.POST:
#         outtime_update_form = OutTimeUpdateForm()  # Instantiate the OutTimeUpdateForm

#     return render(request, 'emp_temp/emp_attend.html', {'form': form, 'outtime_update_form': outtime_update_form, 'employee': employee})

def emp_attend(request):
    user = request.user
    employee = Employee.objects.get(user=user)
    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        if form.is_valid():
            intime = form.cleaned_data['intime']
            outtime = form.cleaned_data['outtime'] 
            date = form.cleaned_data['date']
            

            
            # Check if the date is in the past
            if date < timezone.now().date():
                return HttpResponse("Attendance cannot be recorded for past dates.")
            # Check if the date is in the future
            if date > timezone.now().date():
                return HttpResponse("Attendance cannot be recorded for future Dates.")
            # Check if there is an approved leave request for the same date
            leave_request = LeaveRequest.objects.filter(employee=request.user.employee, date=date, status='approved').first()
            if leave_request:
                return HttpResponse("Attendance cannot be recorded because a leave request for this date is already approved.")
            
            # Check if attendance already exists for the same date
            if Attendance.objects.filter(employee=request.user.employee, date=date).exists():
                return HttpResponse("Attendance for this date already exists.")
            
            company_logic = request.user.employee.company.company_logic

            # Get the weekday of the attendance date (0=Monday, 5=Saturday, 6=Sunday)
            weekday = date.weekday()

            # Check if the attendance date is valid based on company logic
            if company_logic == 'logic1' and weekday >= 5:
                messages.error(request, "Attendance cannot be recorded on weekends for this company.")
                return redirect('emp_attend')
            
            # Calculate late in time, early going time, and late going time
            late_in_time, early_going_time, late_going_time = calculate_late_early(intime, outtime, request.user.employee)
                
            attendance = form.save(commit=False)
            attendance.employee = request.user.employee
            attendance.lateintime = late_in_time  
            attendance.earlygoingtime = early_going_time
            attendance.lategointtime = late_going_time
            attendance.save()
                
            messages.success(request, 'Attendance recorded successfully!')  # Success message
                
            return redirect('emp_attend')
        else:
            messages.error(request, 'Error submitting attendance. Please check the form.')
    else: 
        form = AttendanceForm()
    
    # Initialize outtime_update_form to None by default
    outtime_update_form = None
    
    # Check if intime is posted and no outtime is available
    if 'intime' in request.POST and 'outtime' not in request.POST:
        outtime_update_form = OutTimeUpdateForm()  # Instantiate the OutTimeUpdateForm
    return render(request, 'emp_temp/emp_attend.html', {'form': form, 'outtime_update_form': outtime_update_form , 'employee': employee})





@login_required
def emp_leave(request):
    user = request.user
    employee = Employee.objects.get(user=user)
    if request.method == 'POST':
        form = LeaveRequestForm(request.POST)
        if form.is_valid():
            leave_request = form.save(commit=False)
            leave_request.employee = request.user.employee  # Assuming user is authenticated
            leave_request.save()
            
            messages.success(request, 'Leave application submitted successfully!')
            
            return redirect('emp_leave')  # Redirect to appropriate page after form submission
    else:
        form = LeaveRequestForm()
    return render(request, 'emp_temp/emp_leave.html', {'form': form , 'employee': employee})


@login_required
def view_emp(request):
    users = User.objects.all()
    employees = Employee.objects.select_related('user').all()
    return render(request,'hr_temp/view_emp.html',{'users':users, 'employees':employees})









from datetime import datetime, timedelta


@login_required
def emp_details(request):
    # Retrieve all users from the database
    users = User.objects.all()
    
    # Get the employee_id from the request parameters
    employee_id = request.GET.get('emp_id')

    # Fetch employee details using the employee_id
    try:
        # Retrieve employee details with related user details
        employee = Employee.objects.select_related('user').get(emp_id=employee_id)
        
        # Retrieve attendance records for the specified employee
        employee_attendance = Attendance.objects.filter(employee__emp_id=employee_id)
        
        # Retrieve leave requests for the specified employee
        employee_leave_requests = LeaveRequest.objects.filter(employee__emp_id=employee_id, status='approved')
        
        # Calculate month-wise leave dates, present dates, and total month days
        today = datetime.now()
        current_month = today.month
        current_year = today.year
        days_in_month = calendar.monthrange(current_year, current_month)[1]
        month_start_date = datetime(current_year, current_month, 1)
        month_end_date = datetime(current_year, current_month, days_in_month)
        
        leave_dates = []
        present_dates = []
        
        for day in range(1, days_in_month + 1):
            current_date = datetime(current_year, current_month, day)
            if current_date <= today:
                # Check if the current date is a weekend (Saturday or Sunday)
                if current_date.weekday() >= 5:  # Saturday or Sunday
                    present_dates.append(current_date)
                else:
                    # Check if there's an approved leave request for the employee on this date
                    if employee_leave_requests.filter(date=current_date).exists():
                        leave_dates.append(current_date)
                    else:
                        present_dates.append(current_date)

        total_month_days = len(present_dates) + len(leave_dates)
        
        # Pass all data to the template for rendering
        return render(request, 'hr_temp/emp_details.html', {'users': users, 'employee': employee, 'attendances': employee_attendance, 
                                                             'leave_dates': leave_dates, 'present_dates': present_dates, 'total_month_days': total_month_days})
    except Employee.DoesNotExist:
        # Handle the case where employee with the given ID does not exist
        return HttpResponse("Employee not found")








@login_required
def emp_leavetable(request, emp_id):
    
    # Filter leave requests for the specified employee
    leave_requests = LeaveRequest.objects.filter(employee__emp_id=emp_id)
    return render(request, 'hr_temp/emp_leavetable.html', {'leave_requests': leave_requests})


def view_all(request, emp_id):
    try:
        # Retrieve employee details
        employee = Employee.objects.select_related('user').get(emp_id=emp_id)
        
        # Retrieve attendance records for the specified employee
        employee_attendance = Attendance.objects.filter(employee__emp_id=emp_id)
        
        # Retrieve leave requests for the specified employee
        leave_requests = LeaveRequest.objects.filter(employee__emp_id=emp_id)
        
        # Create a dictionary to store leave requests by date
        leave_requests_by_date = {leave.date: leave for leave in leave_requests}
        
        # Create a dictionary to store attendance records by date
        attendance_by_date = {attendance.date: attendance for attendance in employee_attendance}
        
        # Create a list to store matched data
        matched_data = []
        
        # Iterate over all dates where either attendance or leave request exists
        all_dates = set(leave_requests_by_date.keys()) | set(attendance_by_date.keys())
        for date in sorted(all_dates):
            attendance = attendance_by_date.get(date)
            leave_request = leave_requests_by_date.get(date)
            matched_data.append((date, attendance, leave_request))
        
        # Pass all data to the template for rendering
        return render(request, 'hr_temp/view_all.html', {
            'employee': employee,
            'matched_data': matched_data
        })
    except Employee.DoesNotExist:
        # Handle the case where employee with the given ID does not exist
        return HttpResponse("Employee not found")

def leave_requests(request, leave_type=None):
    form = LeaveRequestForm(request.POST or None)
    previous_leave_types = LeaveRequest.objects.values_list('leave_type', flat=True).distinct()

    if request.method == 'POST':
        form = LeaveRequestForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('leave_requests')  # Redirect to leave request page or any other relevant page

    previous_leave_requests = None
    if leave_type:
        previous_leave_requests = LeaveRequest.objects.filter(leave_type=leave_type)

    return render(request, 'leave_requests.html', {'form': form, 'previous_leave_types': previous_leave_types, 'previous_leave_requests': previous_leave_requests})
    
def get_previous_leave_dates(request):
    if request.method == 'GET':
        leave_type = request.GET.get('leave_type')
        if leave_type:
            # Fetch previous leave dates for the specified leave type
            previous_leave_dates = LeaveRequest.objects.filter(employee=request.user.employee, leave_type=leave_type).values_list('date', flat=True).distinct()
            return JsonResponse(list(previous_leave_dates), safe=False)
    # Return empty response if no leave type is specified or if method is not GET
    return JsonResponse([], safe=False)


def download_employee_details(request, emp_id):
    try:
        # Retrieve employee details
        employee = Employee.objects.select_related('user').get(emp_id=emp_id)
        
        # Retrieve user details for the employee
        user_name = f"{employee.user.first_name} {employee.user.last_name}" if employee.user else ""
        
        # Check if first_name and last_name are not empty
        if employee.first_name and employee.last_name:
            # Remove leading and trailing spaces
            first_name = employee.first_name.strip()
            last_name = employee.last_name.strip()

            # Replace special characters with underscores
            filename = f"{user_name}.csv"
            filename = ''.join(c if c.isalnum() else '_' for c in filename)
        else:
            # If first_name or last_name is empty, set a default filename
            filename = "employee_details.csv"
        
        # Retrieve attendance records for the specified employee
        employee_attendance = Attendance.objects.filter(employee__emp_id=emp_id)
        
        # Retrieve leave requests for the specified employee
        leave_requests = LeaveRequest.objects.filter(employee__emp_id=emp_id)
        
        # Create a dictionary to store leave requests by date
        leave_requests_by_date = {leave.date: leave for leave in leave_requests}
        
        # Create a dictionary to store attendance records by date
        attendance_by_date = {attendance.date: attendance for attendance in employee_attendance}
        
        # Create a list to store matched data
        matched_data = []
        
        # Iterate over all dates where either attendance or leave request exists
        all_dates = set(leave_requests_by_date.keys()) | set(attendance_by_date.keys())
        for date in sorted(all_dates):
            attendance = attendance_by_date.get(date)
            leave_request = leave_requests_by_date.get(date)
            matched_data.append((date, attendance, leave_request))
        
        # Prepare CSV data
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'

        # Write CSV data
        writer = csv.writer(response)
        
        # Write employee name and ID as the first row
        writer.writerow(['Employee Name:', user_name, 'Employee ID:', employee.emp_id])
        writer.writerow([])  # Empty row for separation
        
        writer.writerow(['Date/Day', 'Time In', 'Time Out', 'Late Coming (min)', 'Early Going (min)', 'Remark', 'Leave Type', 'Leave Date', 'Leave Status', 'Leave Remark', 'Leave Created At', 'Leave Updated At'])
        for date, attendance, leave_request in matched_data:
            row = [date]
            if attendance:
                row.extend([attendance.intime, attendance.outtime, attendance.lateintime, attendance.earlygoingtime, attendance.remark])
            else:
                row.extend(['-', '-', '-', '-', '-'])
            if leave_request:
                row.extend([leave_request.leave_type, leave_request.date, leave_request.status, leave_request.leaveremark, leave_request.created_at, leave_request.updated_at])
            else:
                row.extend(['-', '-', '-', '-', '-', '-'])
            writer.writerow(row)

        return response

    except Employee.DoesNotExist:
        return HttpResponse("Employee not found")



def HR_update(request):
    user = request.user

    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST)

        if form.is_valid():
            old_password = form.cleaned_data.get('old_password')
            new_password = form.cleaned_data.get('new_password')
            confirm_password = form.cleaned_data.get('confirm_password')

            # Check if the old password matches the user's current password
            if not user.check_password(old_password):
                messages.error(request, 'Old password is incorrect.')
            else:
                # Update the user's email and username
                user.email = form.cleaned_data.get('email')
                user.username = form.cleaned_data.get('username')

                # If new password is provided and matches the confirmation, update the password
                if new_password and new_password == confirm_password:
                    user.set_password(new_password)
                    user.save()
                    messages.success(request, 'Profile updated successfully, including password.')
                    return redirect('login')  # Redirect to profile update page
                elif new_password and new_password != confirm_password:
                    messages.error(request, 'New password and confirm password do not match.')
                else:
                    user.save()
                    messages.success(request, 'Profile updated successfully.')
                    return redirect('login')  # Redirect to profile update page
    else:
        form = ProfileUpdateForm(initial={'email': user.email, 'username': user.username})  # Initialize form with current user data for GET request

    return render(request, 'hr_temp/update.html', {'form': form})

from django.utils.text import slugify
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from io import BytesIO

def generate_employee_data(employee):
    employee_data = [
        ["Employee ID", employee.emp_id,"Name", f"{employee.first_name} {employee.last_name}"],
        ["Designation" , employee.designation, "Email ID", employee.user.email],
        ["Mobile Number", "9876543210", "Date of Birth", employee.date_of_birth],
        ["Blood Group", employee.blood_group, "PAN Number", employee.pan_no],
        ["Date of Joining", employee.date_of_joining, "Date of Confirmation", employee.date_of_probation],
        ["Company Name", employee.company.company_name, "Salary", employee.salary],
        ["Bank Account No", employee.bank_account_no, "IFSC Code", employee.ifsc_code],
        ["Address", employee.address],
        ["Emergency Contact 1", employee.emg_mobile_no_1,"Emergency Contact 2" ,employee.emg_mobile_no_2],
        ["Relation with Emergency Contact 1", employee.emg_relation_1,"Relation with Emergency Contact 2" ,employee.emg_relation_2],
        
          
    ]
    return employee_data

def generate_attendance_data(employee_attendance):
    attendance_data = [
        ["Date/Day", "Time In", "Time Out", "Late Coming (hr:min)", "Early Going (hr:min)","Late Going (hr:min)", "Remark"]
    ]
    for attendance in employee_attendance:
        attendance_data.append([
            attendance.date,
            attendance.str_intime,
            attendance.str_outtime,
            attendance.str_lateintime,
            attendance.str_earlygoingtime,
            attendance.str_lategointtime,
            attendance.remark
        ])
    return attendance_data


def generate_pdf(request, emp_id):
    try:
        employee = Employee.objects.select_related('user').get(emp_id=emp_id)
        employee_attendance = Attendance.objects.filter(employee__emp_id=emp_id)
        
        buffer = BytesIO()
        pdf = SimpleDocTemplate(buffer, pagesize=letter)
        elements = []

        # Define styles
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            name='Title',
            parent=styles['Title'],
            fontSize=24,
            textColor=colors.black,
            alignment=1,
            spaceAfter=12
        )
        cell_style = ParagraphStyle(
            name='Cell',
            parent=styles['Normal'],
            fontSize=10,
            textColor=colors.black,
            alignment=0,
            spaceAfter=6
        )
        value_bold_style = ParagraphStyle(
            name='ValueBold',
            parent=styles['Normal'],
            fontSize=10,
            textColor=colors.black,
            alignment=0,
            spaceAfter=6,
            fontName='Helvetica-Bold'
        )

        # Add title
        title = Paragraph("Employee Report", title_style)
        elements.append(title)

        # Add employee data
        employee_data = generate_employee_data(employee)
        employee_table_data = []

        for row in employee_data:
            employee_table_data.append([
                Paragraph(str(cell), cell_style) if idx % 2 == 0 else Paragraph(str(cell), value_bold_style)
                for idx, cell in enumerate(row)
            ])

        employee_table = Table(employee_table_data, colWidths=[2 * inch, 2 * inch, 2 * inch, 2 * inch])
        employee_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        elements.append(employee_table)

        # Add attendance data
        attendance_data = generate_attendance_data(employee_attendance)
        attendance_table_data = [
            [Paragraph(str(cell), cell_style) if idx % 2 == 0 else Paragraph(str(cell), value_bold_style)
             for idx, cell in enumerate(row)]
            for row in attendance_data
        ]

        attendance_table = Table(attendance_table_data, colWidths=[1.2 * inch] * 6)
        attendance_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        elements.append(attendance_table)

        # Build PDF...
        pdf.build(elements)

        # Set response content type...
        response = HttpResponse(content_type='application/pdf')

        # Set filename for download
        filename = f"{slugify(employee.user.first_name)}_{slugify(employee.user.last_name)}.pdf"
        response['Content-Disposition'] = f'attachment; filename="{filename}"'

        # Write PDF data to response...
        pdf_data = buffer.getvalue()
        buffer.close()
        response.write(pdf_data)
        return response

    except Employee.DoesNotExist:
        return HttpResponse("Employee not found")



from django.http import HttpResponse
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from django.template.defaultfilters import slugify
from .models import Employee, Attendance  
    

def generate_condensed_employee_data(employee):
    employee_data = [
        ["Employee ID", employee.emp_id,"Name", f"{employee.first_name} {employee.last_name}" ],
        ["Email ID", employee.user.email,"Mobile No",employee.mobile_no],
        ["Company Name", employee.company.company_name, "Designation", employee.designation]
    ]
    return employee_data

def small_report(request, emp_id):
    try:
        employee = Employee.objects.select_related('user').get(emp_id=emp_id)
        employee_attendance = Attendance.objects.filter(employee__emp_id=emp_id)
        
        buffer = BytesIO()
        pdf = SimpleDocTemplate(buffer, pagesize=letter)
        elements = []

        # Define styles
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            name='Title',
            parent=styles['Title'],
            fontSize=24,
            textColor=colors.black,
            alignment=1,
            spaceAfter=12
        )
        cell_style = ParagraphStyle(
            name='Cell',
            parent=styles['Normal'],
            fontSize=10,
            textColor=colors.black,
            alignment=0,
            spaceAfter=6
        )
        value_bold_style = ParagraphStyle(
            name='ValueBold',
            parent=styles['Normal'],
            fontSize=10,
            textColor=colors.black,
            alignment=0,
            spaceAfter=6,
            fontName='Helvetica-Bold'
        )

        # Add title
        title = Paragraph("Condensed Employee Report", title_style)
        elements.append(title)

        # Add condensed employee data
        employee_data = generate_condensed_employee_data(employee)
        employee_table_data = []

        for row in employee_data:
            employee_table_data.append([
                Paragraph(str(cell), cell_style) if idx % 2 == 0 else Paragraph(str(cell), value_bold_style)
                for idx, cell in enumerate(row)
            ])

        employee_table = Table(employee_table_data, colWidths=[2 * inch, 2 * inch, 2 * inch, 2 * inch])
        employee_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        elements.append(employee_table)

        # Add attendance data
        attendance_data = generate_attendance_data(employee_attendance)
        attendance_table_data = [
            [Paragraph(str(cell), cell_style) if idx % 2 == 0 else Paragraph(str(cell), value_bold_style)
             for idx, cell in enumerate(row)]
            for row in attendance_data
        ]

        attendance_table = Table(attendance_table_data, colWidths=[1.2 * inch] * 6)
        attendance_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        elements.append(attendance_table)

        # Build PDF...
        pdf.build(elements)

        # Set response content type...
        response = HttpResponse(content_type='application/pdf')

        # Set filename for download
        filename = f"{slugify(employee.user.first_name)}_{slugify(employee.user.last_name)}_condensed.pdf"
        response['Content-Disposition'] = f'attachment; filename="{filename}"'

        # Write PDF data to response...
        pdf_data = buffer.getvalue()
        buffer.close()
        response.write(pdf_data)
        return response

    except Employee.DoesNotExist:
        return HttpResponse("Employee not found")



from datetime import datetime

import calendar


@login_required
def employee_leave_balance(request, emp_id):
    employee = get_object_or_404(Employee, emp_id=emp_id)
    leave_requests = LeaveRequest.objects.filter(employee=employee)

    # Total leave allocation for the year
    total_cl = employee.CL
    total_sl = employee.SL
    total_pl = employee.PL

    # Initialize leave balance dictionary for each month
    leave_balance_data = {}

    # Initialize leave balance for the year
    cl_balance = total_cl
    sl_balance = total_sl
    pl_balance = total_pl

    # Loop through each month of the year
    for month in range(1, 13):
        month_name = calendar.month_name[month]
        
        # Calculate leaves taken for each month
        cl_leave_taken = leave_requests.filter(date__month=month, leave_type='CL').count()
        sl_leave_taken = leave_requests.filter(date__month=month, leave_type='SL').count()
        pl_leave_taken = leave_requests.filter(date__month=month, leave_type='PL').count()

        # Calculate opening balance for each month
        cl_opening_balance = cl_balance
        sl_opening_balance = sl_balance
        pl_opening_balance = pl_balance

        # Calculate closing balance for each month
        cl_balance -= cl_leave_taken
        sl_balance -= sl_leave_taken
        pl_balance -= pl_leave_taken

        # Store the data for the month
        leave_balance_data[month_name] = {
            'leaves_taken': {'CL': cl_leave_taken, 'SL': sl_leave_taken, 'PL': pl_leave_taken},
            'opening_balance': {'CL': cl_opening_balance, 'SL': sl_opening_balance, 'PL': pl_opening_balance},
            'closing_balance': {'CL': cl_balance, 'SL': sl_balance, 'PL': pl_balance}
        }

    context = {
        'employee': employee,
        'leave_balance_data': leave_balance_data,
    }

    return render(request, 'hr_temp/employee_leave_balance.html', context)












def leavetable(request):
    user = request.user
    employee = Employee.objects.get(user=user)
    # Filter leave requests for the currently logged-in employee
    leave_requests = LeaveRequest.objects.filter(employee=request.user.employee)
    return render(request, 'emp_temp/leavetable.html', {'leave_requests': leave_requests,'employee':employee})


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
import csv
from io import BytesIO
import calendar
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Employee, SalarySlip

def upload_salary_slip(request):
    employees = Employee.objects.all()  # Fetch all employees from the database

    if request.method == 'POST':
        employee_id = request.POST.get('employee_id')
        month_name = request.POST.get('month')
        year = request.POST.get('year')
        salary_slip_file = request.FILES.get('salary_slip_file')

        # Validate inputs
        if not (employee_id and month_name and year and salary_slip_file):
            messages.error(request, 'Please fill all fields.')
            return redirect('upload_salary_slip')

        # Convert month name to its numerical representation
        try:
            month_number = list(calendar.month_name).index(month_name.capitalize())
        except ValueError:
            messages.error(request, 'Invalid month name.')
            return redirect('upload_salary_slip')

        # Check if CSV data is empty
        try:
            csv_data = salary_slip_file.read().decode('utf-8').splitlines()
            if not csv_data:
                raise ValueError
        except (UnicodeDecodeError, ValueError):
            messages.error(request, 'CSV file is empty or improperly formatted.')
            return redirect('upload_salary_slip')

        # Retrieve employee details
        try:
            employee = Employee.objects.get(pk=employee_id)
        except Employee.DoesNotExist:
            messages.error(request, 'Employee does not exist.')
            return redirect('upload_salary_slip')

        # Create PDF
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        elements = []

        styles = getSampleStyleSheet()
        title_style = styles['Title']
        subtitle_style = ParagraphStyle('Subtitle', parent=styles['Title'], fontSize=14, spaceAfter=14)

        # Add company name to the PDF heading
        heading_text = employee.company.company_name
        elements.append(Paragraph(heading_text, title_style))
        elements.append(Paragraph(f"SALARY SLIP FOR THE MONTH OF {month_name.upper()} - {year}", subtitle_style))
        elements.append(Spacer(1, 20))  # Add space between heading and table

        # Read CSV data and prepare table
        csv_reader = csv.reader(csv_data)
        data = list(csv_reader)

        # Define column widths for the table
        col_widths = [100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100]

        # Define the table data for the first 7 rows with 4 columns each, next 6 rows with 5 columns each, and the rest as is
        table_data = []
        for i in range(7):
            row_data = data[i][:5]  # Get first 4 columns for first 7 rows
            table_data.append(row_data)
        for i in range(7, 13):
            row_data = data[i][:6]  # Get first 5 columns for rows 7 to 12
            table_data.append(row_data)
        for i in range(13, len(data)):
            row_data = data[i]  # Keep remaining rows as is
            table_data.append(row_data)

        # Create the table
        table = Table(table_data, colWidths=col_widths)

        # Style the table
        table_style = TableStyle([
            ('LINEABOVE', (0, 0), (-1, 0), 1, colors.black),  # Top border for header
            ('LINEBELOW', (0, 0), (-1, 0), 1, colors.black),  # Bold bottom border for header
            ('LINEABOVE', (0, 7), (-1, 7), 1, colors.black),  # Bold dividing line for row 8
            ('LINEBELOW', (0, 7), (-1, 7), 1, colors.black),  # Bold dividing line for row 8
            ('LINEABOVE', (0, 11), (-1, 11), 1, colors.black),  # Bold dividing line for row 14
            ('LINEBELOW', (0, 11), (-1, 11), 1, colors.black),  # Bold dividing line for row 14
            ('LINEABOVE', (0, 19), (-1, 19), 1, colors.black),
            ('LINEABOVE', (0, 18), (-1, 18), 1, colors.black),
            ('LINEBELOW', (0, 18), (-1, 18),1,colors.black),
            ('LINEBEFORE', (0, 0), (0, -1), 1, colors.black),  # Vertical line before column 0
            ('LINEBEFORE', (3, 0), (3, -1), 1, colors.black),  # Vertical line before column 4
            ('LINEBEFORE', (6, 0), (6, -1), 1, colors.black),  # Vertical line before column 7
            ('LINEAFTER', (5, 0), (5, -1), 1, colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),  # Center alignment for all cells
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),  # Background color for header
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),  # Text color for header
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Bold font for header
            ('FONTSIZE', (0, 0), (-1, -1), 10),  # Set font size
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),  # Padding for header
            ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),  # Background color for cells
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),  # Text color for cells
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),# Regular font for cells
        ])
        table.setStyle(table_style)

        # Add the table to elements list
        elements.append(table)

        # Add the signature line
        signature_text = "This is a computer-generated printout; does not require authorized signature."
        elements.append(Spacer(1, 20))  # Add space between table and signature
        elements.append(Paragraph(signature_text, styles['Italic']))

        # Build PDF
        doc.build(elements)

        # Save PDF to file field in SalarySlip model
        try:
            salary_slip = SalarySlip.objects.create(employee_id=employee_id, month=month_number, year=year)
            salary_slip_file_name = f'salary_slip_{employee_id}_{month_name}_{year}.pdf'
            salary_slip.salary_slip_file.save(salary_slip_file_name, buffer)
            buffer.seek(0)  # Reset buffer position to the beginning

            messages.success(request, 'Salary slip uploaded successfully.')
            return redirect('dashboard')  # Redirect to employee dashboard or any other appropriate page
        except Exception as e:
            messages.error(request, f'Error creating salary slip: {str(e)}')
            return redirect('upload_salary_slip')

    # Pass employees to the template context
    return render(request, 'hr_temp/upload_salary_slip.html', {'employees': employees})

def upload_success(request):
    return render(request, 'hr_temp/upload_salary_slip.html')
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

from django.shortcuts import render, HttpResponse
from .models import SalarySlip, Employee

from calendar import month_name

def view_salary_slips(request, emp_id=None):
    # Retrieve all employees with related user details
    employees = Employee.objects.select_related('user').all()
    
    # Fetch employee details using the emp_id
    if emp_id:
        try:
            employee = Employee.objects.select_related('user').get(emp_id=emp_id)
            
            # Retrieve salary slips for the specified employee
            employee_salary_slips = SalarySlip.objects.filter(employee__emp_id=emp_id)
            
            # Convert month numbers to month names
            for slip in employee_salary_slips:
                slip.month = month_name[slip.month]
            
            # Pass all data to the template for rendering
            return render(request, 'hr_temp/view_salary_slip.html', {'employees': employees, 'employee': employee, 'salary_slips': employee_salary_slips})
        except Employee.DoesNotExist:
            # Handle the case where employee with the given ID does not exist
            return HttpResponse("Employee not found")
    else:
        # Handle the case where emp_id is not provided in the URL parameters
        return HttpResponse("Employee ID not provided")




def salary_slip_overview(request):
    employee = request.user.employee  # Assuming user is logged in and has associated Employee object
    salary_slips = SalarySlip.objects.filter(employee=employee)
    
    return render(request, 'emp_temp/salary_slip_overview.html', {'salary_slips': salary_slips})




def view_salary_slip(request, salary_slip_id):
    salary_slip = get_object_or_404(SalarySlip, id=salary_slip_id)
    
    # Assuming you want to serve the PDF file directly
    with open(salary_slip.pdf_file.path, 'rb') as pdf:
        response = HttpResponse(pdf.read(), content_type='application/pdf')
        response['Content-Disposition'] = f'filename="{salary_slip.pdf_file.name}"'
        return response
    
def salary_detail(request, emp_id):
    user = request.user
    employees = Employee.objects.get(user=user)
    employee = Employee.objects.get(pk=emp_id)
    salary_slips = SalarySlip.objects.filter(employee=employee)

    context = {
        'employees':employees,
        'employee': employee,
        'salary_slips': salary_slips,
    }
    return render(request, 'emp_temp/salary.html', context)

def employee_leave_balance_csv(request, emp_id):
    employee = get_object_or_404(Employee, emp_id=emp_id)
    leave_requests = LeaveRequest.objects.filter(employee=employee)

    total_cl = employee.CL
    total_sl = employee.SL
    total_pl = employee.PL

    leave_balance_data = {}
    cl_balance = total_cl
    sl_balance = total_sl
    pl_balance = total_pl

    for month in range(1, 13):
        month_name = calendar.month_name[month]
        cl_leave_taken = leave_requests.filter(date__month=month, leave_type='CL').count()
        sl_leave_taken = leave_requests.filter(date__month=month, leave_type='SL').count()
        pl_leave_taken = leave_requests.filter(date__month=month, leave_type='PL').count()

        cl_opening_balance = cl_balance
        sl_opening_balance = sl_balance
        pl_opening_balance = pl_balance

        cl_balance -= cl_leave_taken
        sl_balance -= sl_leave_taken
        pl_balance -= pl_leave_taken

        leave_balance_data[month_name] = {
            'leaves_taken': {'CL': cl_leave_taken, 'SL': sl_leave_taken, 'PL': pl_leave_taken},
            'opening_balance': {'CL': cl_opening_balance, 'SL': sl_opening_balance, 'PL': pl_opening_balance},
            'closing_balance': {'CL': cl_balance, 'SL': sl_balance, 'PL': pl_balance}
        }

    # Prepare CSV data
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="leave_balance_{employee.first_name}_{employee.last_name}.csv"'

    # Write CSV data
    writer = csv.writer(response)
    writer.writerow(['Employee Name:', f"{employee.user.first_name} {employee.user.last_name}", 'Employee ID:', employee.emp_id])
    writer.writerow([])  # Empty row for separation
    writer.writerow(['Month', 'CL Opening Balance', 'CL Leaves Taken', 'SL Opening Balance', 'SL Leaves Taken', 'PL Opening Balance', 'PL Leaves Taken', 'CL Closing Balance', 'SL Closing Balance', 'PL Closing Balance'])
    
    for month, data in leave_balance_data.items():
        writer.writerow([
            month,
            data['opening_balance']['CL'],
            data['leaves_taken']['CL'],
            data['opening_balance']['SL'],
            data['leaves_taken']['SL'],
            data['opening_balance']['PL'],
            data['leaves_taken']['PL'],
            data['closing_balance']['CL'],
            data['closing_balance']['SL'],
            data['closing_balance']['PL']
        ])

    return response



import csv
from django.http import HttpResponse
from .models import SalaryDetails

def download_csv(request):

    # Get the selected company name from the GET parameters
    selected_company_name = request.GET.get('company_name')

    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="employee_salaries.csv"'

    writer = csv.writer(response)
    writer.writerow([
        'Employee ID','Employee Name', 'Month', 'Total Days', 'Absent Days', 'Paid Days',
        'Actual Basic', 'Actual HRA', 'Actual Education Allowance',
        'Actual Statutory Bonus', 'Actual Conveyance Allowance', 'Actual Other Allowance',
        'Actual Standard LTA', 'Standard Basic', 'Standard HRA',
        'Standard Education Allowance', 'Standard Statutory Bonus',
        'Standard Conveyance Allowance', 'Other Allowance', 'Standard LTA',
        'Gross', 'Loan Advance', 'LW Fund', 'Standard PF', 'Actual PF',
        'Professional Tax', 'Labor Tax', 'Total Deduction', 'Net Salary', 'ESIC', 'PT Deduction'
    ])

    # Filter salary details based on the selected company
    if selected_company_name:
        employees = Employee.objects.filter(company__company_name=selected_company_name).select_related('user')
        salary_details = SalaryDetails.objects.filter(employee__in=employees)
    else:
        salary_details = SalaryDetails.objects.all()

    # Write the salary details to the CSV file
    for salary in salary_details:
        writer.writerow([
            f"{salary.employee.emp_id}",
            f"{salary.employee.user.first_name} {salary.employee.user.last_name}",
            salary.month,
            salary.total_days, salary.absent_days, salary.paid_days,
            salary.actual_basic, salary.actual_HRA, salary.actual_edu_allowance,
            salary.actual_statutory_bonus, salary.actual_conveyance_allowance, salary.actual_other_allowance,
            salary.actual_standard_LTA, salary.standard_basic, salary.standard_HRA,
            salary.standard_edu_allowance, salary.standard_statutory_bonus,
            salary.standard_conveyance_allowance, salary.other_allowance, salary.standard_LTA,
            salary.gross, salary.loan_advance, salary.lw_fund, salary.standard_pf, salary.actual_pf,
            salary.p_tax, salary.l_tax, salary.total_deduction, salary.net_salary, salary.ESIC, salary.pt_deduction
        ])

    return response



# -------------------------------------------------------------------------------------------------------------------------------------------




from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.utils import timezone
from django.db import transaction
from .models import Employee, SalaryDetails
from datetime import datetime
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect

@login_required
@csrf_protect
def salarysheet(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'update':
            with transaction.atomic():  # Ensure atomic transaction for data consistency
                num_entries = (len(request.POST) - 1) // 30  # Assuming 30 fields per salary entry

                for i in range(num_entries):
                    salary_id = request.POST.get(f'salary_{i}_id')
                    salary_data = {
                        'month': None,
                        'total_days': request.POST.get(f'salary_{i}_total_days', 0),
                        'absent_days': request.POST.get(f'salary_{i}_absent_days', 0),
                        'paid_days': request.POST.get(f'salary_{i}_paid_days', 0),
                        'actual_basic': request.POST.get(f'salary_{i}_actual_basic', 0),
                        'actual_HRA': request.POST.get(f'salary_{i}_actual_HRA', 0),
                        'actual_edu_allowance': request.POST.get(f'salary_{i}_actual_edu_allowance', 0),
                        'actual_statutory_bonus': request.POST.get(f'salary_{i}_actual_statutory_bonus', 0),
                        'actual_conveyance_allowance': request.POST.get(f'salary_{i}_actual_conveyance_allowance', 0),
                        'actual_other_allowance': request.POST.get(f'salary_{i}_actual_other_allowance', 0),
                        'actual_standard_LTA': request.POST.get(f'salary_{i}_actual_standard_LTA', 0),
                        'standard_basic': request.POST.get(f'salary_{i}_standard_basic', 0),
                        'standard_HRA': request.POST.get(f'salary_{i}_standard_HRA', 0),
                        'standard_edu_allowance': request.POST.get(f'salary_{i}_standard_edu_allowance', 0),
                        'standard_statutory_bonus': request.POST.get(f'salary_{i}_standard_statutory_bonus', 0),
                        'standard_conveyance_allowance': request.POST.get(f'salary_{i}_standard_conveyance_allowance', 0),
                        'other_allowance': request.POST.get(f'salary_{i}_other_allowance', 0),
                        'standard_LTA': request.POST.get(f'salary_{i}_standard_LTA', 0),
                        'gross': request.POST.get(f'salary_{i}_gross', 0),
                        'loan_advance': request.POST.get(f'salary_{i}_loan_advance', 0),
                        'lw_fund': request.POST.get(f'salary_{i}_lw_fund', 0),
                        'standard_pf': request.POST.get(f'salary_{i}_standard_pf', 0),
                        'actual_pf': request.POST.get(f'salary_{i}_actual_pf', 0),
                        'p_tax': request.POST.get(f'salary_{i}_p_tax', 0),
                        'l_tax': request.POST.get(f'salary_{i}_l_tax', 0),
                        'total_deduction': request.POST.get(f'salary_{i}_total_deduction', 0),
                        'net_salary': request.POST.get(f'salary_{i}_net_salary', 0),
                        'ESIC': request.POST.get(f'salary_{i}_ESIC', 0),
                        'pt_deduction': request.POST.get(f'salary_{i}_pt_deduction', 0),
                    }

                    try:
                        # Handle date conversion for 'month' field
                        month_str = request.POST.get(f'salary_{i}_month')
                        if month_str:
                            salary_data['month'] = datetime.strptime(month_str, '%Y-%m-%d').date()
                        else:
                            salary_data['month'] = None  # Or set to a default value as needed
                    except ValueError:
                        # Handle the case where the date string is not in the expected format
                        salary_data['month'] = None

                    # Convert numeric fields to floats
                    for key in salary_data:
                        if key != 'month':  # Skip date field
                            try:
                                salary_data[key] = float(salary_data[key])
                            except ValueError:
                                salary_data[key] = 0.0  # Handle empty or invalid values

                    try:
                        # Update or create the salary details in the database
                        salary_instance, created = SalaryDetails.objects.update_or_create(id=salary_id, defaults=salary_data)
                        
                        # Update corresponding Employee instance's standard fields
                        employee = salary_instance.employee
                        employee.standard_basic = salary_data['standard_basic']
                        employee.standard_HRA = salary_data['standard_HRA']
                        employee.standard_edu_allowance = salary_data.get('standard_edu_allowance', 0)
                        employee.standard_statutory_bonus = salary_data.get('standard_statutory_bonus', 0)
                        employee.standard_conveyance_allowance = salary_data.get('standard_conveyance_allowance', 0)
                        employee.other_allowance = salary_data.get('other_allowance', 0)
                        employee.standard_LTA = salary_data.get('standard_LTA', 0)
                        employee.save()

                    except ValidationError as e:
                        # Handle validation errors here, e.g., log the error or return an error response
                        return render(request, 'error_page.html', {'error_message': str(e)})
                    

                    employee.last_modified = timezone.now()
                    employee.save()

                return redirect('salarysheet')  # Redirect after successful update

    # Handle GET request or other logic (fetching data for display in the form)
    selected_company_name = request.GET.get('company_name')
    companies = Company.objects.all()

    if selected_company_name:
        employees = Employee.objects.filter(company__company_name=selected_company_name).select_related('user')
    else:
        employees = Employee.objects.select_related('user').all()

    employee_salary_details = []

    for employee in employees:
        salaries = SalaryDetails.objects.filter(employee=employee)
        salary_details = {
            'employee': employee,
            'salaries': salaries,
        }
        employee_salary_details.append(salary_details)

    context = {
        'employee_salary_details': employee_salary_details,
        'companies': companies,
        'selected_company_name': selected_company_name,
    }
    return render(request, 'hr_temp/salarysheet.html', context)



# views.py

from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from datetime import datetime
import calendar
from .models import Employee, SalaryDetails, LeaveRequest, Company



def pdf_generate(request, emp_id):
    # Create a buffer to store PDF content
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    user = request.user
    employee = get_object_or_404(Employee, emp_id=emp_id)
    salary_details = SalaryDetails.objects.filter(employee=employee).latest('month')
    company = Company.objects.first()

    month_start_date = datetime(salary_details.month.year, salary_details.month.month, 1)
    month_end_date = datetime(salary_details.month.year, salary_details.month.month, calendar.monthrange(salary_details.month.year, salary_details.month.month)[1])

    employee_leave_requests = LeaveRequest.objects.filter(employee=employee, status='approved', date__range=(month_start_date, month_end_date))

    cl_leaves_taken = employee_leave_requests.filter(leave_type='CL').count()
    sl_leaves_taken = employee_leave_requests.filter(leave_type='SL').count()
    pl_leaves_taken = employee_leave_requests.filter(leave_type='PL').count()

    cl_opening_balance = employee.CL - LeaveRequest.objects.filter(employee=employee, leave_type='CL', date__lt=month_start_date).count()
    sl_opening_balance = employee.SL - LeaveRequest.objects.filter(employee=employee, leave_type='SL', date__lt=month_start_date).count()
    pl_opening_balance = employee.PL - LeaveRequest.objects.filter(employee=employee, leave_type='PL', date__lt=month_start_date).count()

    cl_balance = cl_opening_balance - cl_leaves_taken
    sl_balance = sl_opening_balance - sl_leaves_taken
    pl_balance = pl_opening_balance - pl_leaves_taken
    salary_month_year = salary_details.month.strftime('%B %Y')

    # Title for the PDF
    title = f"{company.company_name}"
    story = [Paragraph(title, styles['Title'])]
    story.append(Paragraph(f"SALARY SLIP FOR THE MONTH OF - {salary_month_year}", styles['Title']))

    net_salary = salary_details.net_salary
    net_salary_words = convert_to_words(net_salary)

    # Prepare data for the first table (Employee Information)
    table_data_employee = [
        [f'Salary for {salary_month_year}', '', 'Employee ID', employee.emp_id],
        [Paragraph('<b>Employee Name:</b>', styles['Normal']), Paragraph(f"{employee.user.first_name} {employee.user.last_name}", styles['Normal']),
         Paragraph('<b>Designation:</b>', styles['Normal']), Paragraph(employee.designation, styles['Normal'])],
        [Paragraph('<b>Date of Joining:</b>', styles['Normal']), Paragraph(str(employee.date_of_joining), styles['Normal']),
         Paragraph('<b>Date of Probation:</b>', styles['Normal']), Paragraph(str(employee.date_of_probation), styles['Normal'])],
        [Paragraph('<b>UAN Number:</b>', styles['Normal']), Paragraph(employee.emp_id, styles['Normal']),
         Paragraph('<b>Aadhaar Number:</b>', styles['Normal']), Paragraph(str(employee.aadhaar), styles['Normal'])],
        [Paragraph('<b>PAN Card Number:</b>', styles['Normal']), Paragraph(employee.pan_no, styles['Normal']),
         Paragraph('<b>Bank Name:</b>', styles['Normal']), Paragraph(employee.bank, styles['Normal'])],
        [Paragraph('<b>Account Number:</b>', styles['Normal']), Paragraph(str(employee.bank_account_no), styles['Normal']),
         Paragraph('<b>Date of Birth:</b>', styles['Normal']), Paragraph(str(employee.date_of_birth), styles['Normal'])],
        [Paragraph('<b>Company Name:</b>', styles['Normal']), Paragraph(employee.company.company_name, styles['Normal']), '', '']
    ]

    # Create a table for Employee Information and style
    table_employee = Table(table_data_employee, colWidths=[150, 150, 150, 150], repeatRows=1, hAlign='CENTER')
    table_employee.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
    ]))

    # Add Employee Information table to the story
    story.append(table_employee)

    # Prepare data for the second table (Attendance and Leave Details)
    attendance_data = [
        ['', '', '', '', '', ''],
        [Paragraph('<b>Month Days</b>', styles['Normal']), Paragraph('<b></b>', styles['Normal']),
         Paragraph('<b>Leaves</b>', styles['Normal']), Paragraph('<b>Opening Balance</b>', styles['Normal']),
         Paragraph('<b>Leaves Taken</b>', styles['Normal']), Paragraph('<b>Closing Balance</b>', styles['Normal'])],
        ['Present', salary_details.paid_days, 'Sick Leave', sl_opening_balance, sl_leaves_taken, sl_balance],
        ['Absent', salary_details.absent_days, 'Casual Leave', cl_opening_balance, cl_leaves_taken, cl_balance],
        ['Total', salary_details.total_days, 'Privilege Leave', pl_opening_balance, pl_leaves_taken, pl_balance],
        ['', '', '', '', '', '']
    ]

    # Create a table for Attendance and Leave Details and style
    table_attendance = Table(attendance_data, colWidths=[100, 100, 100, 100, 100, 100], repeatRows=1, hAlign='CENTER')
    table_attendance.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
    ]))

    # Add Attendance and Leave Details table to the story
    story.append(table_attendance)

    # Create the additional row with 2 columns spanning the entire table width
    additional_row_data = [
        [Paragraph('<b>Earnings</b>', styles['Normal']), Paragraph('<b>Deductions</b>', styles['Normal'])]
    ]

    # Create a table for the additional row and style
    additional_row = Table(additional_row_data, colWidths=[300, 300], hAlign='CENTER')
    additional_row.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),   # Center align all cells horizontally
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # Center align all cells vertically
        ('GRID', (0, 0), (-1, -1), 1, colors.black),  # Add grid with black color
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Bold font for the first row
    ]))

    # Add the additional row to the story
    story.append(additional_row)

    # Prepare data for the third table (Salary Details)
    salary_table_data = [
        [Paragraph('<b></b>', styles['Normal']), Paragraph('<b>Standard</b>', styles['Normal']),
         Paragraph('<b>Actual</b>', styles['Normal']), Paragraph('<b></b>', styles['Normal']),
         Paragraph('<b>Standard</b>', styles['Normal']), Paragraph('<b>Actual</b>', styles['Normal'])],
        ['Basic Pay', salary_details.standard_basic, salary_details.actual_basic, 'PF', salary_details.standard_pf, salary_details.actual_pf],
        ['HRA', salary_details.standard_HRA, salary_details.actual_HRA, 'PT', salary_details.pt_deduction, salary_details.pt_deduction],
        ['Education Allowance', salary_details.standard_edu_allowance, salary_details.actual_edu_allowance, 'LWF', '', salary_details.lw_fund],
        ['Statutory Bonus', salary_details.standard_statutory_bonus, salary_details.actual_statutory_bonus, 'ESIC', '', salary_details.ESIC],
        ['LTA', salary_details.standard_LTA, salary_details.actual_standard_LTA, 'Income Tax', '', salary_details.l_tax],
        ['Conveyance', salary_details.standard_conveyance_allowance, salary_details.actual_conveyance_allowance, 'Loan', '', ''],
        ['', '', '', '', '', ''],
        [Paragraph('<b>Total Earnings</b>', styles['Normal']), salary_details.gross, '', Paragraph('<b>Total Deduction</b>', styles['Normal']), '', salary_details.total_deduction],
        [Paragraph('<b>Net Salary</b>', styles['Normal']), salary_details.net_salary, '', '', '', '']
    ]

    # Create a table for Salary Details and style
    table_salary = Table(salary_table_data, colWidths=[100, 100, 100, 100, 100, 100], repeatRows=1, hAlign='CENTER')
    table_salary.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
    ]))

    # Add Salary Details table to the story
    story.append(table_salary)

    # Add separate table with one column and one row
    one_cell_table_data = [[Paragraph(f'<b>In Words:</b> {net_salary_words} Only', styles['Normal'])]]
    table_one_cell = Table(one_cell_table_data, colWidths=[sum([100, 100, 100, 100, 100, 100])], hAlign='CENTER')
    table_one_cell.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ]))

    # Add the one-cell table to the story
    story.append(Spacer(1, 12))
    story.append(table_one_cell)
    story.append(Spacer(1, 12))

    # Add text below the table
    story.append(Paragraph('This is a computer-generated document. No signature is required.', styles['Normal']))

    # Build PDF
    doc.build(story)

    # Get PDF content from buffer
    pdf_content = buffer.getvalue()
    buffer.close()

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Salary_Slip_{salary_month_year}.pdf"'
    response.write(pdf_content)

    return response





# views.py
# views.py

from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponse
from django.core.files.base import ContentFile
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from datetime import date, datetime
import calendar

from .models import Employee, SalaryDetails, LeaveRequest

def pdf_upload(request, emp_id):
    # Retrieve the employee object
    employee = get_object_or_404(Employee, emp_id=emp_id)
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    
    # Retrieve the latest salary details for the employee
    try:
        salary_details = SalaryDetails.objects.filter(employee=employee).latest('month')
    except SalaryDetails.DoesNotExist:
        return HttpResponse('Salary details not found for this employee.')

    # Calculate leave balances for the month
    month_start_date = date(salary_details.month.year, salary_details.month.month, 1)
    month_end_date = date(salary_details.month.year, salary_details.month.month, calendar.monthrange(salary_details.month.year, salary_details.month.month)[1])

    employee_leave_requests = LeaveRequest.objects.filter(employee=employee, status='approved', date__range=(month_start_date, month_end_date))
    
    cl_leaves_taken = employee_leave_requests.filter(leave_type='CL').count()
    sl_leaves_taken = employee_leave_requests.filter(leave_type='SL').count()
    pl_leaves_taken = employee_leave_requests.filter(leave_type='PL').count()

    cl_opening_balance = employee.CL - LeaveRequest.objects.filter(employee=employee, leave_type='CL', date__lt=month_start_date).count()
    sl_opening_balance = employee.SL - LeaveRequest.objects.filter(employee=employee, leave_type='SL', date__lt=month_start_date).count()
    pl_opening_balance = employee.PL - LeaveRequest.objects.filter(employee=employee, leave_type='PL', date__lt=month_start_date).count()
    
    cl_balance = employee.CL - cl_leaves_taken
    sl_balance = employee.SL - sl_leaves_taken
    pl_balance = employee.PL - pl_leaves_taken
    salary_month_year = salary_details.month.strftime('%B %Y')
    # Title for the PDF
    title = f"{employee.company.company_name}"
    story = [Paragraph(title, styles['Title'])]
    story.append(Paragraph(f"SALARY SLIP FOR THE MONTH OF - {salary_month_year}", styles['Title']))
    
    net_salary = salary_details.net_salary
    net_salary_words = convert_to_words(net_salary)

    # Prepare data for the first table (Employee Information)
    table_data_employee = [
        [ f'Salary for {salary_month_year}','', 'Employee ID', employee.emp_id],
        [Paragraph('<b>Employee Name:</b>', styles['Normal']), Paragraph(f"{employee.user.first_name} {employee.user.last_name}", styles['Normal']),
         Paragraph('<b>Designation:</b>', styles['Normal']), Paragraph(employee.designation, styles['Normal'])],
        [Paragraph('<b>Date of Joining:</b>', styles['Normal']), Paragraph(str(employee.date_of_joining), styles['Normal']),
         Paragraph('<b>Date of Probation:</b>', styles['Normal']), Paragraph(str(employee.date_of_probation), styles['Normal'])],
        [Paragraph('<b>UAN Number:</b>', styles['Normal']), Paragraph(employee.emp_id, styles['Normal']),
         Paragraph('<b>Aadhaar Number:</b>', styles['Normal']), Paragraph(str(employee.aadhaar), styles['Normal'])],
        [Paragraph('<b>PAN Card Number:</b>', styles['Normal']), Paragraph(employee.pan_no, styles['Normal']),
         Paragraph('<b>Bank Name:</b>', styles['Normal']), Paragraph(employee.bank, styles['Normal'])],
        [Paragraph('<b>Account Number:</b>', styles['Normal']), Paragraph(str(employee.bank_account_no), styles['Normal']),
         Paragraph('<b>Date of Birth:</b>', styles['Normal']), Paragraph(str(employee.date_of_birth), styles['Normal'])],
        [Paragraph('<b>Company Name:</b>', styles['Normal']), Paragraph(employee.company.company_name, styles['Normal']), '', '']
    ]

    # Create a table for Employee Information and style
    table_employee = Table(table_data_employee, colWidths=[150, 150, 150, 150], repeatRows=1, hAlign='CENTER')
    table_employee.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
    ]))

    # Add Employee Information table to the story
    story.append(table_employee)

    # Prepare data for the second table (Attendance and Leave Details)
    attendance_data = [
        ['', '', '', '', '', ''],
        [Paragraph('<b>Month Days</b>', styles['Normal']), Paragraph('<b></b>', styles['Normal']),
         Paragraph('<b>Leaves</b>', styles['Normal']), Paragraph('<b>Opening Balance</b>', styles['Normal']),
         Paragraph('<b>Leaves Taken</b>', styles['Normal']), Paragraph('<b>Closing Balance</b>', styles['Normal'])],
        ['Present', salary_details.paid_days, 'Sick Leave', sl_opening_balance, sl_leaves_taken, sl_balance],
        ['Absent', salary_details.absent_days, 'Casual Leave', cl_opening_balance, cl_leaves_taken, cl_balance],
        ['Total', salary_details.total_days, 'Privilege Leave', pl_opening_balance, pl_leaves_taken, pl_balance],
        ['', '', '', '', '', '']
    ]

    # Create a table for Attendance and Leave Details and style
    table_attendance = Table(attendance_data, colWidths=[100, 100, 100, 100, 100, 100], repeatRows=1, hAlign='CENTER')
    table_attendance.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
    ]))

    # Add Attendance and Leave Details table to the story
    story.append(table_attendance)

    # Create the additional row with 2 columns spanning the entire table width
    additional_row_data = [
        
        [Paragraph('<b>Earnings</b>', styles['Normal']), Paragraph('<b>Deductions</b>', styles['Normal'])]
    ]

    # Create a table for the additional row and style
    additional_row = Table(additional_row_data, colWidths=[300, 300], hAlign='CENTER')
    additional_row.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),   # Center align all cells horizontally
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # Center align all cells vertically
        ('GRID', (0, 0), (-1, -1), 1, colors.black),  # Add grid with black color
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Bold font for the first row
    ]))


    # Add the additional row to the story
    story.append(additional_row)

    # Prepare data for the third table (Salary Details)
    salary_table_data = [
        
        [Paragraph('<b></b>', styles['Normal']), Paragraph('<b>Standard</b>', styles['Normal']),
         Paragraph('<b>Actual</b>', styles['Normal']), Paragraph('<b></b>', styles['Normal']),
         Paragraph('<b>Standard</b>', styles['Normal']), Paragraph('<b>Actual</b>', styles['Normal'])],
        
        ['Basic Pay', salary_details.standard_basic, salary_details.actual_basic, 'PF', salary_details.standard_pf, salary_details.actual_pf],
        ['HRA', salary_details.standard_HRA, salary_details.actual_HRA, 'PT', salary_details.pt_deduction, salary_details.pt_deduction],
        ['Education Allowance', salary_details.standard_edu_allowance, salary_details.actual_edu_allowance, 'LWF', '', salary_details.lw_fund],
        ['Statutory Bonus', salary_details.standard_statutory_bonus, salary_details.actual_statutory_bonus, 'ESIC', '', salary_details.ESIC],
        ['LTA', salary_details.standard_LTA, salary_details.actual_standard_LTA, 'Income Tax', '', salary_details.l_tax],
        ['Loan', '', '', 'Loan', '', ''],
        ['', '', '', '', '', ''],
        [Paragraph('<b>Total Earnings</b>', styles['Normal']), salary_details.gross, '', Paragraph('<b>Total Deduction</b>', styles['Normal']), '', salary_details.total_deduction],
        [Paragraph('<b>Net Salary</b>', styles['Normal']),salary_details.net_salary,'','','','']
    ]

    # Create a table for Salary Details and style
    table_salary = Table(salary_table_data, colWidths=[100, 100, 100, 100, 100, 100], repeatRows=1, hAlign='CENTER')
    table_salary.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
    ]))

    # Add Salary Details table to the story
    story.append(table_salary)

    # Add separate table with one column and one row
    one_cell_table_data = [[Paragraph(f'<b>In Words:</b> {net_salary_words} Only', styles['Normal'])]]
    table_one_cell = Table(one_cell_table_data, colWidths=[sum([100, 100, 100, 100, 100, 100])], hAlign='CENTER')
    table_one_cell.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ]))

    # Add the one-cell table to the story
    story.append(Spacer(1, 12))
    story.append(table_one_cell)
    story.append(Spacer(1, 12))

    # Add text below the table
    story.append(Paragraph('This is a computer-generated document. No signature is required.', styles['Normal']))

    # In Words section
    

    # Note section
    

    # Build PDF
    doc.build(story)

    # Get PDF content from buffer
    pdf_content = buffer.getvalue()
    buffer.close()

    # Save PDF file to SalarySlip model
    salary_slip = SalarySlip(employee=employee, month=date.today(), pdf_file=ContentFile(pdf_content, name=f"{employee.emp_id}_salary_slip.pdf"))
    salary_slip.save()

    return redirect('salarysheet')


from django.db import IntegrityError
from django.shortcuts import render, redirect
from .models import EmployeeJoining

def add_employee(request):
    if request.method == 'POST':
        emp_id = request.POST['emp_id']
        first_name = request.POST['first_name']
        middle_name = request.POST.get('middle_name', '')
        last_name = request.POST['last_name']
        email = request.POST['email']
        contact_number = request.POST['contact_number']
        whatsapp_number = request.POST.get('whatsapp_number', '')
        age = request.POST['age']
        gender = request.POST['gender']
        current_address = request.POST['current_address']
        permanent_address = request.POST['permanent_address']
        city = request.POST['city']
        state = request.POST['state']
        pincode = request.POST['pincode']
        security_guard_training = request.POST.get('security_guard_training') == 'yes'
        job_experience = request.POST.get('job_experience') == 'yes'
        profile_picture = request.FILES['profile_picture']
        signature = request.FILES['signature']
        preferred_work_arrangements = request.POST['preferred_work_arrangements']
        position = request.POST['position']
        account_holder_name = request.POST['account_holder_name']
        bank_name = request.POST['bank_name']
        bank_account_number = request.POST['bank_account_number']
        ifsc_code = request.POST['ifsc_code']
        branch_name = request.POST['branch_name']
        bank_address = request.POST['bank_address']
        qualification = request.POST['qualification']
        experience = request.POST['experience']

        try:
            employee = EmployeeJoining(
                emp_id=emp_id,
                first_name=first_name,
                middle_name=middle_name,
                last_name=last_name,
                email=email,
                contact_number=contact_number,
                whatsapp_number=whatsapp_number,
                age=age,
                gender=gender,
                current_address=current_address,
                permanent_address=permanent_address,
                city=city,
                state=state,
                pincode=pincode,
                security_guard_training=security_guard_training,
                job_experience=job_experience,
                profile_picture=profile_picture,
                signature=signature,
                preferred_work_arrangements=preferred_work_arrangements,
                position=position,
                account_holder_name=account_holder_name,
                bank_name=bank_name,
                bank_account_number=bank_account_number,
                ifsc_code=ifsc_code,
                branch_name=branch_name,
                bank_address=bank_address,
                qualification=qualification,
                experience=experience
            )
            employee.save()
            return redirect('add_employee')  # Redirect to a success page after saving
        except IntegrityError:
            return render(request, 'hr_temp/employee_form.html', {'error': 'Employee ID already exists. Please use a unique Employee ID.'})

    return render(request, 'hr_temp/employee_form.html')



    
