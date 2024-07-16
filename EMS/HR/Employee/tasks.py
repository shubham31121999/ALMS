from celery import shared_task
from datetime import datetime, timedelta
from django.utils import timezone
import calendar
import logging
from .models import Attendance, SalaryDetails, Employee, LeaveRequest
from celery import shared_task
from datetime import datetime, time, timedelta
from .models import Employee, Attendance, LeaveRequest

import calendar
from datetime import datetime
from django.db.models import Sum

logger = logging.getLogger(__name__)

@shared_task
def update_employee_availability():
    employees = Employee.objects.all()
    for employee in employees:
        # Update the fields
        logger.info(f"Updating employee {employee.id}: late_min_ava to 90, late_time_ava to 90 minutes")
        employee.late_min_ava = 90
        employee.late_time_ava = timedelta(minutes=90)
        # Save the changes to the database
        employee.save() 
        logger.info(f"Employee {employee.id} updated successfully")


@shared_task
def generate_salary():
    today = timezone.now().date()
    yesterday = today - timedelta(days=1)

    employees = Employee.objects.all()
    for employee in employees:
        calculate_employee_salary(employee, yesterday.month, yesterday.year)

# def calculate_employee_salary(employee, month, year):
#     # Calculate total leaves, present days, and working days
#     days_in_month = calendar.monthrange(year, month)[1]
#     month_start_date = datetime(year, month, 1)
#     month_end_date = datetime(year, month, days_in_month)

#     employee_leave_requests = LeaveRequest.objects.filter(employee=employee, status='approved', date__range=(month_start_date, month_end_date))
#     employee_attendance = Attendance.objects.filter(employee=employee, date__range=(month_start_date, month_end_date))

#     total_leaves = employee_leave_requests.count()
#     total_present_days = employee_attendance.count()
#     total_working_days = days_in_month  # Assuming all days are working days, adjust as needed

#     cl_opening_balance = employee.CL - LeaveRequest.objects.filter(employee=employee, leave_type='CL', date__lt=month_start_date).count()
#     sl_opening_balance = employee.SL - LeaveRequest.objects.filter(employee=employee, leave_type='SL', date__lt=month_start_date).count()
#     pl_opening_balance = employee.PL - LeaveRequest.objects.filter(employee=employee, leave_type='PL', date__lt=month_start_date).count()

#     cl_leaves_taken = employee_leave_requests.filter(leave_type='CL').count()
#     sl_leaves_taken = employee_leave_requests.filter(leave_type='SL').count()
#     pl_leaves_taken = employee_leave_requests.filter(leave_type='PL').count()

#     # Calculate leave balance
#     cl_balance = employee.CL - cl_leaves_taken
#     sl_balance = employee.SL - sl_leaves_taken
#     pl_balance = employee.PL - pl_leaves_taken

#     # Calculate standard salary (assuming integer calculations)
#     standard_basic = employee.standard_basic
#     standard_HRA = employee.standard_HRA
#     standard_edu_allowance = employee.standard_edu_allowance
#     standard_statutory_bonus = employee.standard_statutory_bonus
#     standard_LTA = employee.standard_LTA
#     standard_conveyance_allowance = employee.standard_conveyance_allowance
#     # Add other standard salary components here

#     # Calculate actual salary
#     actual_basic = round((employee.standard_basic / days_in_month) * total_present_days if employee.standard_basic is not None else 0)
#     actual_HRA = round((employee.standard_HRA / days_in_month) * total_present_days if employee.standard_HRA is not None else 0)
#     actual_edu_allowance = round((employee.standard_edu_allowance / days_in_month) * total_present_days if employee.standard_edu_allowance is not None else 0)
#     actual_statutory_bonus = round((employee.standard_statutory_bonus / days_in_month) * total_present_days if employee.standard_statutory_bonus is not None else 0)
#     actual_LTA = round((employee.standard_LTA / days_in_month) * total_present_days if employee.standard_LTA is not None else 0)
#     actual_conveyance_allowance = round((employee.standard_conveyance_allowance / days_in_month) * total_present_days if employee.standard_conveyance_allowance is not None else 0)
#     # Add other actual salary components here

#     gross = (
#         actual_basic + actual_HRA +
#         actual_edu_allowance + actual_statutory_bonus + actual_LTA + actual_conveyance_allowance
#         # Add other components here
#     )

#     actual_pf = 0.12 * actual_basic if actual_basic is not None else 0
#     pt_deduction = 200 if month != 2 else 300
#     lw_fund = 25 if month in [6, 12] else 0
#     ESIC = gross * 0.0075

#     total_deduction = (
#         actual_pf +
#         pt_deduction +
#         lw_fund +
#         ESIC
#         # Add other deductions as needed
#     )

#     net_salary = round(gross - total_deduction)

#     # Create or update SalaryDetails instance
#     salary_details, created = SalaryDetails.objects.get_or_create(
#         employee=employee,
#         month=month_start_date,
#         defaults={
#             'standard_basic': standard_basic,
#             'standard_HRA': standard_HRA,
#             'standard_edu_allowance': standard_edu_allowance,
#             'standard_statutory_bonus': standard_statutory_bonus,
#             'standard_LTA': standard_LTA,
#             'standard_conveyance_allowance': standard_conveyance_allowance,
#             'total_days': total_working_days,
#             'absent_days': total_leaves,
#             'paid_days': total_present_days,
#             'actual_basic': actual_basic,
#             'actual_HRA': actual_HRA,
#             'actual_edu_allowance': actual_edu_allowance,
#             # Add other fields here
#             'gross': gross,
#             'actual_pf': actual_pf,
#             'pt_deduction': pt_deduction,
#             'lw_fund': lw_fund,
#             'ESIC': ESIC,
#             'total_deduction': total_deduction,
#             'net_salary': net_salary
#         }
#     )

#     if not created:
#         # Update existing instance
#         salary_details.standard_basic = standard_basic
#         salary_details.standard_HRA = standard_HRA
#         salary_details.standard_edu_allowance = standard_edu_allowance
#         salary_details.standard_statutory_bonus = standard_statutory_bonus
#         salary_details.standard_LTA = standard_LTA
#         salary_details.standard_conveyance_allowance = standard_conveyance_allowance
#         salary_details.total_days = total_working_days
#         salary_details.absent_days = total_leaves
#         salary_details.paid_days = total_present_days
#         salary_details.actual_basic = actual_basic
#         salary_details.actual_HRA = actual_HRA
#         salary_details.actual_edu_allowance = actual_edu_allowance
#         # Update other fields here
#         salary_details.gross = gross
#         salary_details.actual_pf = actual_pf
#         salary_details.pt_deduction = pt_deduction
#         salary_details.lw_fund = lw_fund
#         salary_details.ESIC = ESIC
#         salary_details.total_deduction = total_deduction
#         salary_details.net_salary = net_salary
#         salary_details.save()

# def calculate_employee_salary(employee, month, year):
#     # Calculate total leaves, present days, and working days
#     days_in_month = calendar.monthrange(year, month)[1]
#     month_start_date = datetime(year, month, 1)
#     month_end_date = datetime(year, month, days_in_month)
    
    
#     employee_leave_requests = LeaveRequest.objects.filter(employee=employee, status='approved', date__range=(month_start_date, month_end_date))
#     employee_attendance = Attendance.objects.filter(employee=employee, date__range=(month_start_date, month_end_date))

#     total_leaves = employee_leave_requests.count()
#     total_present_days = employee_attendance.count()
#     total_working_days = days_in_month  # Assuming all days are working days, adjust as needed

#     cl_opening_balance = employee.CL - LeaveRequest.objects.filter(employee=employee, leave_type='CL', date__lt=month_start_date).count()
#     sl_opening_balance = employee.SL - LeaveRequest.objects.filter(employee=employee, leave_type='SL', date__lt=month_start_date).count()
#     pl_opening_balance = employee.PL - LeaveRequest.objects.filter(employee=employee, leave_type='PL', date__lt=month_start_date).count()

#     cl_leaves_taken = employee_leave_requests.filter(leave_type='CL').count()
#     sl_leaves_taken = employee_leave_requests.filter(leave_type='SL').count()
#     pl_leaves_taken = employee_leave_requests.filter(leave_type='PL').count()

#     # Calculate leave balance
#     cl_balance = employee.CL - cl_leaves_taken
#     sl_balance = employee.SL - sl_leaves_taken
#     pl_balance = employee.PL - pl_leaves_taken

#     # Calculate standard salary (assuming integer calculations)
#     standard_basic = employee.standard_basic
#     standard_HRA = employee.standard_HRA
#     standard_edu_allowance = employee.standard_edu_allowance
#     standard_statutory_bonus = employee.standard_statutory_bonus
#     standard_LTA = employee.standard_LTA
#     standard_conveyance_allowance = employee.standard_conveyance_allowance
#     # Add other standard salary components here

#     # Calculate actual salary
#     actual_basic = round((employee.standard_basic / days_in_month) * total_present_days if employee.standard_basic is not None else 0)
#     actual_HRA = round((employee.standard_HRA / days_in_month) * total_present_days if employee.standard_HRA is not None else 0)
#     actual_edu_allowance = round((employee.standard_edu_allowance / days_in_month) * total_present_days if employee.standard_edu_allowance is not None else 0)
#     actual_statutory_bonus = round((employee.standard_statutory_bonus / days_in_month) * total_present_days if employee.standard_statutory_bonus is not None else 0)
#     actual_LTA = round((employee.standard_LTA / days_in_month) * total_present_days if employee.standard_LTA is not None else 0)
#     actual_conveyance_allowance = round((employee.standard_conveyance_allowance / days_in_month) * total_present_days if employee.standard_conveyance_allowance is not None else 0)
#     # Add other actual salary components here

#     gross = (
#         actual_basic + actual_HRA +
#         actual_edu_allowance + actual_statutory_bonus + actual_LTA + actual_conveyance_allowance
#         # Add other components here
#     )

#     actual_pf = 0.12 * actual_basic if actual_basic is not None else 0
#     pt_deduction = 200 if month != 2 else 300
#     lw_fund = 25 if month in [6, 12] else 0
#     ESIC = gross * 0.0075

#     total_deduction = (
#         actual_pf +
#         pt_deduction +
#         lw_fund +
#         ESIC
#         # Add other deductions as needed
#     )

#     net_salary = round(gross - total_deduction)

#     # Retrieve or create SalaryDetails instance for the employee and month
#     salary_details, created = SalaryDetails.objects.get_or_create(
#         employee=employee,
#         month=month_start_date,
#         defaults={
#             'standard_basic': standard_basic,
#             'standard_HRA': standard_HRA,
#             'standard_edu_allowance': standard_edu_allowance,
#             'standard_statutory_bonus': standard_statutory_bonus,
#             'standard_LTA': standard_LTA,
#             'standard_conveyance_allowance': standard_conveyance_allowance,
#             'total_days': total_working_days,
#             'absent_days': total_leaves,
#             'paid_days': total_present_days,
#             'actual_basic': actual_basic,
#             'actual_HRA': actual_HRA,
#             'actual_edu_allowance': actual_edu_allowance,
#             # Add other fields here
#             'gross': gross,
#             'actual_pf': actual_pf,
#             'pt_deduction': pt_deduction,
#             'lw_fund': lw_fund,
#             'ESIC': ESIC,
#             'total_deduction': total_deduction,
#             'net_salary': net_salary
#         }
#     )

#     if not created:
#         # Update existing instance with new values
#         salary_details.standard_basic = standard_basic
#         salary_details.standard_HRA = standard_HRA
#         salary_details.standard_edu_allowance = standard_edu_allowance
#         salary_details.standard_statutory_bonus = standard_statutory_bonus
#         salary_details.standard_LTA = standard_LTA
#         salary_details.standard_conveyance_allowance = standard_conveyance_allowance
#         salary_details.total_days = total_working_days
#         salary_details.absent_days = total_leaves
#         salary_details.paid_days = total_present_days
#         salary_details.actual_basic = actual_basic
#         salary_details.actual_HRA = actual_HRA
#         salary_details.actual_edu_allowance = actual_edu_allowance
#         # Update other fields here
#         salary_details.gross = gross
#         salary_details.actual_pf = actual_pf
#         salary_details.pt_deduction = pt_deduction
#         salary_details.lw_fund = lw_fund
#         salary_details.ESIC = ESIC
#         salary_details.total_deduction = total_deduction
#         salary_details.net_salary = net_salary
#         salary_details.save()



def calculate_employee_salary(employee, month, year):
    # Calculate total leaves, present days, and working days
    days_in_month = calendar.monthrange(year, month)[1]
    month_start_date = datetime(year, month, 1)
    month_end_date = datetime(year, month, days_in_month)
    
    # Retrieve leave requests and attendance
    employee_leave_requests = LeaveRequest.objects.filter(employee=employee, status='approved', date__range=(month_start_date, month_end_date))
    employee_attendance = Attendance.objects.filter(employee=employee, date__range=(month_start_date, month_end_date))

    total_leaves = employee_leave_requests.count()
    total_present_days = employee_attendance.count()
    total_working_days = days_in_month  # Adjust if weekends/holidays are not working days

    # Calculate leave balances
    cl_opening_balance = employee.CL - LeaveRequest.objects.filter(employee=employee, leave_type='CL', date__lt=month_start_date).count()
    sl_opening_balance = employee.SL - LeaveRequest.objects.filter(employee=employee, leave_type='SL', date__lt=month_start_date).count()
    pl_opening_balance = employee.PL - LeaveRequest.objects.filter(employee=employee, leave_type='PL', date__lt=month_start_date).count()

    cl_leaves_taken = employee_leave_requests.filter(leave_type='CL').count()
    sl_leaves_taken = employee_leave_requests.filter(leave_type='SL').count()
    pl_leaves_taken = employee_leave_requests.filter(leave_type='PL').count()

    cl_balance = employee.CL - cl_leaves_taken
    sl_balance = employee.SL - sl_leaves_taken
    pl_balance = employee.PL - pl_leaves_taken

    # Calculate standard salary components
    standard_basic = employee.standard_basic
    standard_HRA = employee.standard_HRA
    standard_edu_allowance = employee.standard_edu_allowance
    standard_statutory_bonus = employee.standard_statutory_bonus
    standard_LTA = employee.standard_LTA
    standard_conveyance_allowance = employee.standard_conveyance_allowance

    # Calculate actual salary components
    actual_basic = round((standard_basic / days_in_month) * total_present_days) if standard_basic is not None else 0
    actual_HRA = round((standard_HRA / days_in_month) * total_present_days) if standard_HRA is not None else 0
    actual_edu_allowance = round((standard_edu_allowance / days_in_month) * total_present_days) if standard_edu_allowance is not None else 0
    actual_statutory_bonus = round((standard_statutory_bonus / days_in_month) * total_present_days) if standard_statutory_bonus is not None else 0
    actual_standard_LTA = round((standard_LTA / days_in_month) * total_present_days) if standard_LTA is not None else 0
    actual_conveyance_allowance = round((standard_conveyance_allowance / days_in_month) * total_present_days) if standard_conveyance_allowance is not None else 0

    # Debug statements
    print(f"Standard Statutory Bonus: {standard_statutory_bonus}, Actual Statutory Bonus: {actual_statutory_bonus}")
    print(f"Standard LTA: {standard_LTA}, Actual LTA: {actual_standard_LTA}")
    print(f"Standard Conveyance Allowance: {standard_conveyance_allowance}, Actual Conveyance Allowance: {actual_conveyance_allowance}")

    # Calculate gross salary
    gross = (
        actual_basic + actual_HRA +
        actual_edu_allowance + actual_statutory_bonus + actual_standard_LTA + actual_conveyance_allowance
        # Add other components here
    )

    # Calculate deductions
    actual_pf = 0.12 * actual_basic if actual_basic is not None else 0
    pt_deduction = 200 if month != 2 else 300
    lw_fund = 25 if month in [6, 12] else 0
    ESIC = gross * 0.0075

    total_deduction = (
        actual_pf +
        pt_deduction +
        lw_fund +
        ESIC
        # Add other deductions as needed
    )

    net_salary = round(gross - total_deduction)

    # Retrieve or create SalaryDetails instance for the employee and month
    salary_details, created = SalaryDetails.objects.get_or_create(
        employee=employee,
        month=month_start_date,
        defaults={
            'standard_basic': standard_basic,
            'standard_HRA': standard_HRA,
            'standard_edu_allowance': standard_edu_allowance,
            'standard_statutory_bonus': standard_statutory_bonus,
            'standard_LTA': standard_LTA,
            'standard_conveyance_allowance': standard_conveyance_allowance,
            'total_days': total_working_days,
            'absent_days': total_leaves,
            'paid_days': total_present_days,
            'actual_basic': actual_basic,
            'actual_HRA': actual_HRA,
            'actual_edu_allowance': actual_edu_allowance,
            'actual_statutory_bonus': actual_statutory_bonus,
            'actual_standard_LTA': actual_standard_LTA,
            'actual_conveyance_allowance': actual_conveyance_allowance,
            'gross': gross,
            'actual_pf': actual_pf,
            'pt_deduction': pt_deduction,
            'lw_fund': lw_fund,
            'ESIC': ESIC,
            'total_deduction': total_deduction,
            'net_salary': net_salary
        }
    )

    if not created:
        # Update existing instance with new values
        salary_details.standard_basic = standard_basic
        salary_details.standard_HRA = standard_HRA
        salary_details.standard_edu_allowance = standard_edu_allowance
        salary_details.standard_statutory_bonus = standard_statutory_bonus
        salary_details.standard_LTA = standard_LTA
        salary_details.standard_conveyance_allowance = standard_conveyance_allowance
        salary_details.total_days = total_working_days
        salary_details.absent_days = total_leaves
        salary_details.paid_days = total_present_days
        salary_details.actual_basic = actual_basic
        salary_details.actual_HRA = actual_HRA
        salary_details.actual_edu_allowance = actual_edu_allowance
        salary_details.actual_statutory_bonus = actual_statutory_bonus
        salary_details.actual_standard_LTA = actual_standard_LTA
        salary_details.actual_conveyance_allowance = actual_conveyance_allowance
        salary_details.gross = gross
        salary_details.actual_pf = actual_pf
        salary_details.pt_deduction = pt_deduction
        salary_details.lw_fund = lw_fund
        salary_details.ESIC = ESIC
        salary_details.total_deduction = total_deduction
        salary_details.net_salary = net_salary
        salary_details.save()



@shared_task
def check_employee_attendance_and_deduct_leave():
    # Get current date and time
    now = datetime.now()
    current_date = now.date()
    current_time = now.time()
    
    # Check if the current time is after 5:00 PM
    if current_time >= time(hour=5, minute=0):
        # Get all employees
        employees = Employee.objects.all()
        
        for employee in employees:
            # Check if the employee has attendance for today and intime is recorded
            try:
                attendance = Attendance.objects.get(employee=employee, date=current_date, intime__isnull=False)
                # Employee has recorded intime, do nothing
            except Attendance.DoesNotExist:
                # Check if there is an active leave request for the employee today
                active_leave_request = LeaveRequest.objects.filter(employee=employee, start_date__lte=current_date, end_date__gte=current_date).exists()
                
                if not active_leave_request:
                    # Deduct leave days for the employee
                    deduct_leave_for_employee(employee)


@shared_task
def deduct_leave_for_employee(employee):
    # Deduct 1 day from CL if available
    if employee.CL > 0:
        employee.deduct_leave('CL', 1)
        print(f"Deducted 1 day from Casual Leave (CL) for employee {employee.id} on {datetime.now()}")
    # Deduct 1 day from SL if CL is not available
    elif employee.SL > 0:
        employee.deduct_leave('SL', 1)
        print(f"Deducted 1 day from Sick Leave (SL) for employee {employee.id} on {datetime.now()}")
    # Deduct 1 day from PL if SL and CL are not available
    elif employee.PL > 0:
        employee.deduct_leave('PL', 1)
        print(f"Deducted 1 day from Paid Leave (PL) for employee {employee.id} on {datetime.now()}")
    # Add 1 day to UL if CL, SL, and PL are not available
    else:
        employee.UL += 1
        employee.save()
        print(f"Added 1 day to Unpaid Leave (UL) for employee {employee.id} on {datetime.now()}")