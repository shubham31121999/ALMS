from django.db import models
import datetime
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from datetime import time
from datetime import timedelta
from django.contrib.auth.models import User
from calendar import monthrange
from django.db import models, transaction
from django.utils import timezone
from django.core.exceptions import ValidationError
import Employee
from django.db.models import Sum
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.postgres.fields import JSONField

class Holiday(models.Model):
    date = models.DateField(unique=True)
    description = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.date}: {self.description}"
    

class EmployeeJoining(models.Model):
    emp_id = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    contact_number = models.CharField(max_length=15)
    whatsapp_number = models.CharField(max_length=15, blank=True, null=True)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=10)
    current_address = models.TextField()
    permanent_address = models.TextField()
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    pincode = models.CharField(max_length=10)
    security_guard_training = models.CharField(max_length=3, choices=[('yes', 'Yes'), ('no', 'No')], default='no')
    job_experience = models.CharField(max_length=3, choices=[('yes', 'Yes'), ('no', 'No')], default='no')
    profile_picture = models.ImageField(upload_to='profile_pictures/')
    signature = models.ImageField(upload_to='signatures/')
    preferred_work_arrangements = models.CharField(max_length=20)
    position = models.CharField(max_length=50)
    account_holder_name = models.CharField(max_length=100)
    bank_name = models.CharField(max_length=100)
    bank_account_number = models.CharField(max_length=30)
    ifsc_code = models.CharField(max_length=15)
    branch_name = models.CharField(max_length=100)
    bank_address = models.TextField()
    qualification = models.CharField(max_length=20)
    experience = models.CharField(max_length=20)
    
    def __str__(self):
        return self.emp_id

    





class Company(models.Model):
    WORKING_DAYS_CHOICES = [
        ('logic1', 'Monday to Friday'),
        ('logic2', 'Monday to Saturday')
    ]
    company_name = models.CharField(max_length=100)
    company_logic = models.CharField(max_length=10, choices=WORKING_DAYS_CHOICES)
    company_intime = models.TimeField()
    company_outtime = models.TimeField()
    company_logo = models.ImageField(upload_to='company_logos/', blank=True)  # New field

    def __str__(self):
        return f"{self.company_name} ({self.get_company_logic_display()})"

    class Meta:
        verbose_name_plural = "Companies"
        ordering = ['company_name']






class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    reporting = models.CharField(max_length = 100)
    bank = models.CharField(max_length=30)
    email2 = models.EmailField(max_length = 100)
    emp_id = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=200)
    TITLE = [
        ('Mr', 'Mr'),
        ('Mrs', 'Mrs'),
        ('Ms', 'Ms'),
        ('Miss','Miss'),
    ]
    title = models.CharField(max_length=10,choices=TITLE)
    late_min_ava = models.IntegerField(default=90)  # This field tracks the available late minutes per month
    late_time_ava = models.DurationField(default=timedelta(minutes=90))  # This field tracks the same value as a duration  
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    mobile_no = models.IntegerField()
    emg_mobile_no_1 = models.IntegerField()  # First emergency mobile number
    emg_mobile_no_2 = models.IntegerField()  # Second emergency mobile number
    emg_relation_1 = models.CharField(max_length=100)  # Relation for the first emergency contact
    emg_relation_2 = models.CharField(max_length=100)  # Relation for the second emergency contact
    pan_no = models.CharField(max_length=100)
    aadhaar = models.BigIntegerField()
    designation = models.CharField(max_length=100)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    cintime = models.TimeField()
    
    couttime = models.TimeField()
    address = models.TextField(max_length=200)
    current_address = models.TextField(max_length=200)
    salary = models.BigIntegerField()
    standard_basic = models.BigIntegerField()
    standard_HRA = models.BigIntegerField()
    standard_edu_allowance = models.BigIntegerField()
    standard_statutory_bonus = models.BigIntegerField()
    standard_conveyance_allowance = models.BigIntegerField()
    standard_LTA = models.BigIntegerField()
    other_allowance = models.BigIntegerField()
    aadhar_image = models.ImageField(upload_to='media/images/', blank=True)
    pancard_image = models.ImageField(upload_to='media/images/', blank=True)
    bank_account_no = models.BigIntegerField()
    ifsc_code = models.CharField(max_length=100)
    leave_requests = models.ForeignKey('LeaveRequest', on_delete=models.CASCADE, related_name='employee_leave_requests', blank=True, null=True)
    BLOOD_GROUP_CHOICES = [
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
    ]
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUP_CHOICES)
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    MARITAL_STATUS = [
        ('Single', 'Single'),
        ('Married', 'Married'),
        ('Divorced', 'Divorced'),
        

    ]
    EMI_CHOICES = [
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
        (6, '6'),
        (7, '7'),
        (8, '8'),
        (9, '9'),
        (10, '10'),
        (11, '11'),
        (12, '12'),
    ]
    loanamount = models.DecimalField(max_digits=10, decimal_places=2,null=True, blank=True)
    emi = models.IntegerField(choices=EMI_CHOICES)
    emi_per_month = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    marital_status = models.CharField(max_length=20,choices=MARITAL_STATUS)
    anniversary_date = models.DateField( null = True,blank=True)
    date_of_birth = models.DateField()
    date_of_joining = models.DateField()
    date_of_probation = models.DateField()
    password = models.CharField(max_length=100)
    profile_picture = models.ImageField(upload_to='media/images/', null=True, blank=True)
    annual_ctc = models.IntegerField(max_length= 40)
    nominee = models.CharField(max_length=20)
    nominee_relation = models.CharField(max_length=20)
    CL = models.IntegerField(default=0)
    SL = models.IntegerField(default=0)
    PL = models.IntegerField(default=0)
    UL = models.IntegerField(default=0)
    wfh_count = models.IntegerField(default=0)
    od_count = models.IntegerField(default=0)
    objects = models.Manager()
    
    def deduct_leave(self, leave_type, days):
        """
        Deducts the specified number of leave days from the corresponding leave balance.
        If CL, SL, and PL are finished, add remaining days to UL.
        """
        if leave_type == 'CL':
            if self.CL >= days:
                self.CL -= days
            else:
                remaining_days = days - self.CL
                self.UL += remaining_days
                self.CL = 0
        elif leave_type == 'SL':
            if self.SL >= days:
                self.SL -= days
            else:
                remaining_days = days - self.SL
                self.UL += remaining_days
                self.SL = 0
        elif leave_type == 'PL':
            if self.PL >= days:
                self.PL -= days
            else:
                remaining_days = days - self.PL
                self.UL += remaining_days
                self.PL = 0
        elif leave_type == 'UL':
            pass  # UL is not directly deducted
        self.save()

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.emp_id})"
    
    

    @receiver(post_save, sender=Employee)
    def create_employee_salary_details(sender, instance, created, **kwargs):
        if created:
            print(f"Creating salary details for: {instance.first_name} {instance.last_name}")
            current_date = datetime.now()
            last_day_of_last_month = current_date.replace(day=1) - timedelta(days=1)
            num_days_in_last_month = monthrange(last_day_of_last_month.year, last_day_of_last_month.month)[1]

            SalaryDetails.objects.create(
                employee=instance,
                month=last_day_of_last_month,
                total_days=num_days_in_last_month,
                absent_days=0,
                paid_days=num_days_in_last_month,
                actual_basic=0,
                actual_HRA=0,
                actual_edu_allowance=0,
                actual_statutory_bonus=0,
                actual_conveyance_allowance=0,
                actual_other_allowance=0,
                actual_standard_LTA=0,
                standard_basic=instance.standard_basic,
                standard_HRA=instance.standard_HRA,
                standard_edu_allowance=instance.standard_edu_allowance,
                standard_statutory_bonus=instance.standard_statutory_bonus,
                standard_conveyance_allowance=instance.standard_conveyance_allowance,
                other_allowance=instance.other_allowance,
                standard_LTA=instance.standard_LTA,
                gross=0,
                loan_advance=0,
                lw_fund=0,
                standard_pf=0,
                actual_pf=0,
                p_tax=0,
                l_tax=0,
                total_deduction=0,
                net_salary=0
            )
            print(f"Salary details created for: {instance.first_name} {instance.last_name}")




from .models import Employee

class TravelExpense(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    sr_no = models.IntegerField()
    from_place = models.CharField(max_length=100)
    from_date = models.DateField()
    to_place = models.CharField(max_length=100)
    to_date = models.DateField()
    purpose = models.CharField(max_length=200)
    distance = models.DecimalField(max_digits=10, decimal_places=2)
    model_of_travel = models.CharField(max_length=100)
    food_price = models.IntegerField()
    transport_fare = models.IntegerField()
    accommodation = models.IntegerField()
    other = models.IntegerField()
    total = models.IntegerField()
    miscellaneous = models.IntegerField()

    # Add batch_id field
    batch_id = models.IntegerField(null=True, blank=True)

    # def save(self, *args, **kwargs):
    #     if not self.batch_id:
    #         self.batch_id = self.generate_batch_id()
    #     self.calculate_total()  # Calculate total before saving
    #     super().save(*args, **kwargs)

    def save(self, *args, **kwargs):
        if not self.batch_id:
            self.batch_id = self.generate_batch_id()

        # Ensure fields are integers
        self.food_price = int(self.food_price)
        self.transport_fare = int(self.transport_fare)
        self.accommodation = int(self.accommodation)
        self.other = int(self.other)

        self.calculate_total()  # Calculate total before saving
        super().save(*args, **kwargs)

    def calculate_total(self):
        # Calculate total by summing up individual expenses
        self.total = self.food_price + self.transport_fare + self.accommodation + self.other
        print(f"Food Price: {self.food_price}, Transport Fare: {self.transport_fare}, Accommodation: {self.accommodation}, Other: {self.other}, Total: {self.total}")

    def generate_batch_id(self):
        # Find the maximum batch_id in the database and return a new unique batch_id
        max_batch_id = TravelExpense.objects.aggregate(models.Max('batch_id'))['batch_id__max'] or 0
        return max_batch_id + 1

    def __str__(self):
        return f"{self.employee.user.first_name} - {self.purpose} - Total: {self.total}"


class Receipt(models.Model):
    travel_expense = models.ForeignKey(TravelExpense, on_delete=models.CASCADE, related_name='receipts')
    image = models.ImageField(upload_to='media/')

    

class ExpenseReport(models.Model):
    emp_id = models.CharField(max_length=100)
    emp_name = models.CharField(max_length=100)
    date_created = models.DateTimeField()
    pdf_file = models.FileField(upload_to='media/')




class SalaryDetails(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    month = models.DateField()

    total_days = models.IntegerField()
    absent_days = models.IntegerField()
    paid_days = models.IntegerField()
    
    # Actual fields
    actual_basic = models.DecimalField(max_digits=10, decimal_places=2)
    actual_HRA = models.DecimalField(max_digits=10, decimal_places=2)
    actual_edu_allowance = models.DecimalField(max_digits=10, decimal_places=2, blank=True,null=True)
    actual_statutory_bonus = models.DecimalField(max_digits=10, decimal_places=2, blank=True,null=True)
    actual_conveyance_allowance = models.DecimalField(max_digits=10, decimal_places=2, blank=True,null=True)
    actual_other_allowance = models.DecimalField(max_digits=10, decimal_places=2, blank=True,null=True)
    actual_standard_LTA = models.DecimalField(max_digits=10, decimal_places=2, blank=True,null=True)
    
    # Standard fields
    standard_basic = models.DecimalField(max_digits=10, decimal_places=2)
    standard_HRA = models.DecimalField(max_digits=10, decimal_places=2)
    standard_edu_allowance = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    standard_statutory_bonus = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    standard_conveyance_allowance = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    other_allowance = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    standard_LTA = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    
    # Calculated fields
    gross = models.DecimalField(max_digits=10, decimal_places=2)
    loan_advance = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    lw_fund = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    standard_pf = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    actual_pf = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    p_tax = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    l_tax = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    total_deduction = models.DecimalField(max_digits=10, decimal_places=2)
    net_salary = models.DecimalField(max_digits=10, decimal_places=2)
    ESIC = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    pt_deduction = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    

    def save_salary_details(employee, month, total_days, absent_days, paid_days, actual_basic, actual_HRA, actual_edu_allowance,
                        actual_statutory_bonus, actual_conveyance_allowance, actual_other_allowance, actual_standard_LTA,
                        standard_basic, standard_HRA, standard_edu_allowance, standard_statutory_bonus, standard_conveyance_allowance,
                        other_allowance, standard_LTA, gross, loan_advance, lw_fund, standard_pf, actual_pf, p_tax, l_tax,
                        total_deduction, net_salary):
        
        SalaryDetails.objects.create(
        employee=employee,
        month=month,
        total_days=total_days,
        absent_days=absent_days,
        paid_days=paid_days,
        actual_basic=actual_basic,
        actual_HRA=actual_HRA,
        actual_edu_allowance=actual_edu_allowance,
        actual_statutory_bonus=actual_statutory_bonus,
        actual_conveyance_allowance=actual_conveyance_allowance,
        actual_other_allowance=actual_other_allowance,
        actual_standard_LTA=actual_standard_LTA,
        standard_basic=standard_basic,
        standard_HRA=standard_HRA,
        standard_edu_allowance=standard_edu_allowance,
        standard_statutory_bonus=standard_statutory_bonus,
        standard_conveyance_allowance=standard_conveyance_allowance,
        other_allowance=other_allowance,
        standard_LTA=standard_LTA,
        gross=gross,
        loan_advance=loan_advance,
        lw_fund=lw_fund,
        standard_pf=standard_pf,
        actual_pf=actual_pf,
        p_tax=p_tax,
        l_tax=l_tax,
        total_deduction=total_deduction,
        net_salary=net_salary
    )


class SalarySlip(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    month = models.DateField()
    pdf_file = models.FileField(upload_to='salary_pdfs/')

    def __str__(self):
        return f"Salary Slip - {self.employee} - {self.month.strftime('%B %Y')}"

class LeaveRequest(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField()
    LEAVE_CHOICES = [
        ('CL', 'Casual Leave'),
        ('SL', 'Sick Leave'),
        ('PL', 'Paid Leave'),
        ('UL', 'Unpaid Leave')
    ]
    leave_type = models.CharField(max_length=2, choices=LEAVE_CHOICES)
    leaveremark = models.TextField(blank=True)
    hrleaveremark =models.TextField(blank=True)
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected')
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        """
        Custom validation to ensure that the requested days are not negative.
        """
        if self.days_requested < 0:
            raise ValidationError("Number of requested days cannot be negative.")

    def approve(self):
        """
        Approve the leave request and deduct the requested days from the corresponding leave balance.
        """
        if self.status == 'pending':
            self.status = 'approved'
            self.employee.deduct_leave(self.leave_type, self.days_requested)
            self.save()

    def reject(self):
        """
        Reject the leave request.
        """
        if self.status == 'pending':
            self.status = 'rejected'
            self.save()
    
    @property
    def days_requested(self):
        """
        Calculate the number of days requested in the leave request.
        """
        return 1

    def __str__(self):
        return f"{self.employee.first_name} - Leave Request - {self.date}"



class Attendance(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    
    date = models.DateField()
    wfhstatus = models.CharField(max_length=3, blank=True, null=True)
    wfhodremark = models.CharField(max_length=100, blank=True, null=True)
    intime = models.TimeField(blank=True, null=True)
    outtime = models.TimeField(blank=True, null=True)
    lateintime = models.TimeField(blank=True, null=True)
    earlygoingtime = models.TimeField(blank=True, null=True)
    lategointtime = models.TimeField(blank=True, null=True)
    str_intime = models.CharField(max_length=8, blank=True)
    str_lateintime = models.CharField(max_length=8, blank=True)
    str_earlygoingtime = models.CharField(max_length=8, blank=True)
    str_lategointtime = models.CharField(max_length=8, blank=True)

    str_outtime = models.CharField(max_length=8, blank=True)
    remark = models.CharField(max_length=100)
    is_leave_request = models.ForeignKey(LeaveRequest, on_delete=models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):

        

        if self.outtime and self.intime and self.outtime < self.intime:
            raise ValidationError("Out time cannot be earlier than in time")
        

        
    def save(self, *args, **kwargs):

        
        company_logic = self.employee.company.company_logic
        weekday = self.date.weekday()

        if company_logic == 'logic1' and weekday >= 5:
            raise ValidationError("Attendance cannot be recorded on weekends for this company.")
        # if self.date < timezone.now().date():
        #     raise ValidationError("Attendance date cannot be in the past")
        
       

        
        
        if self.wfhstatus and self.wfhodremark:  # If WFH/OD data is provided
            # Set intime and outtime to None for WFH/OD entries
            self.intime = None
            self.outtime = None
            # If is_leave_request exists and it's approved, don't save attendance
            if self.is_leave_request and self.is_leave_request.status == 'approved':
                return
        else:  # If regular daily attendance data is provided
            # Convert time fields to datetime.time objects if they are integers
            if isinstance(self.intime, int):
                self.intime = time(hour=self.intime // 60, minute=self.intime % 60)
            if isinstance(self.outtime, int):
                self.outtime = time(hour=self.outtime // 60, minute=self.outtime % 60)
            if isinstance(self.lateintime, int):
                self.lateintime = time(hour=self.lateintime // 60, minute=self.lateintime % 60)
            if isinstance(self.earlygoingtime, int):
                self.earlygoingtime = time(hour=self.earlygoingtime // 60, minute=self.earlygoingtime % 60)
            if isinstance(self.lategointtime, int):
                self.lategointtime = time(hour=self.lategointtime // 60, minute=self.lategointtime % 60)
                
            


            # Check if the employee is going early or late based on outtime
            if self.outtime and self.employee.couttime:
        # Convert outtime and couttime to timedelta objects
                if isinstance(self.outtime, time):
                    outtime = timedelta(hours=self.outtime.hour, minutes=self.outtime.minute)
                else:
                    outtime = timedelta(minutes=self.outtime)

                if isinstance(self.employee.couttime, time):
                    couttime = timedelta(hours=self.employee.couttime.hour, minutes=self.employee.couttime.minute)
                else:
                    couttime = timedelta(minutes=self.employee.couttime)

                # Check if the employee is leaving early or going late
                if outtime < couttime:
    # Employee is leaving early
                    earlygoing_delta = couttime - outtime
                    self.earlygoingtime = (datetime.datetime.min + earlygoing_delta).time()  # Corrected line
                    self.lateintime = None
                elif outtime > couttime:
    # Employee is going late
                    lategoingtime_delta = outtime - couttime
                    self.lategointtime = (datetime.datetime.min + lategoingtime_delta).time()  # Corrected line
                    self.earlygoingtime = None

                else:
                    self.earlygoingtime = None
                    self.lategointime = None


        
        
        

        if self.intime:
            self.str_intime = self.intime.strftime('%H:%M')  # Format: HH:MM
        if self.outtime:
            self.str_outtime = self.outtime.strftime('%H:%M')
        if self.lateintime:
            self.str_lateintime = self.lateintime.strftime('%H:%M')

        if self.earlygoingtime:
            self.str_earlygoingtime = self.earlygoingtime.strftime('%H:%M')

        if self.lategointtime:
            self.str_lategointtime = self.lategointtime.strftime('%H:%M')

        if self.intime and self.employee.cintime:
            intime_minutes = self.intime.hour * 60 + self.intime.minute
            cintime_minutes = self.employee.cintime.hour * 60 + self.employee.cintime.minute
            lateintime_minutes = intime_minutes - cintime_minutes

            
            if lateintime_minutes > 0:
                hours, remainder = divmod(lateintime_minutes, 60)
                self.lateintime = time(hour=hours, minute=remainder)
                self.employee.late_min_ava -= lateintime_minutes
            else:
                self.lateintime = None

            
            self.employee.late_min_ava = max(0, self.employee.late_min_ava)

            
            self.employee.save()
            

        

        super().save(*args, **kwargs)
    def __str__(self):
        if self.is_leave_request:
            return f"{self.employee.first_name} - Leave Request - {self.date}"
        else:
            return f"{self.employee.first_name} - Attendance - {self.date}"
        



class userCompany(models.Model):
    comId = models.CharField(max_length=50)
    comName = models.CharField(max_length=50)
    comGST = models.CharField(max_length=50)
    comCIN = models.CharField(max_length=50)
    comCont = models.IntegerField()
    comEmail = models.CharField(max_length=50)
    comDLNum1 = models.CharField(max_length=50)
    comDLNum2 = models.CharField(max_length=50)
    comPanNum = models.CharField(max_length=50)
    comAdd = models.CharField(max_length=50)
    comCity = models.TextField(max_length=50)
    comState = models.TextField(max_length=50)
    comPin = models.IntegerField(max_length=50)
    
    def __str__(self):
        return f"{self.comName} {self.comCity} ({self.comId})"

