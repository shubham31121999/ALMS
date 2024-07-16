from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Employee,Attendance,LeaveRequest
from django.core.files import File
from .models import Company

import logging
from django.utils import timezone
from datetime import datetime
from datetime import date, datetime
from django import forms
from .models import Holiday
from .models import Attendance
from django.db import models
from django.forms import inlineformset_factory
from django.db import transaction
from django.utils import timezone

from django import forms

from .models import Attendance
from datetime import timedelta
logger = logging.getLogger(__name__)


class EmployeeAttendanceForm(forms.Form):
    employee = forms.ModelChoiceField(queryset=Employee.objects.all(), required=False, label="Employee")

class HolidayForm(forms.ModelForm):
    class Meta:
        model = Holiday
        fields = ['date', 'description']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.TextInput(attrs={'placeholder': 'Holiday description'}),
        }

# from .models import TravelExpense

# class TravelExpenseForm(forms.ModelForm):
#     class Meta:
#         model = TravelExpense
#         fields = ['sr_no', 'from_place', 'from_date', 'to_place', 'to_date', 'purpose', 'distance',
#                   'model_of_travel', 'food_price', 'transport_fare', 'accommodation', 'other','miscellaneous']
#         widgets = {
#             'from_date': forms.DateInput(attrs={'type': 'date'}),
#             'to_date': forms.DateInput(attrs={'type': 'date'}),
#             'model_of_travel': forms.Select(choices=[('Car', 'Car'),('Bus','Bus'), ('Train', 'Train'), ('Flight', 'Flight')]),
#         }
# TravelExpenseFormSet = inlineformset_factory(Employee, TravelExpense, form = TravelExpenseForm, extra = 1, can_delete = True)


# class EmployeeUpdateForm(forms.ModelForm):
#     class Meta:
#         model = Employee
#         exclude = ('user',)  # Exclude the user field since it's a OneToOneField

#     # Additional fields from the related User model
#     first_name = forms.CharField(max_length=100)
#     last_name = forms.CharField(max_length=100)
#     email = forms.EmailField(max_length=200)

#     def __init__(self, *args, **kwargs):
#         super(EmployeeUpdateForm, self).__init__(*args, **kwargs)
#         # Set initial values for fields from the related User model
#         if self.instance.user:
#             self.initial['first_name'] = self.instance.user.first_name
#             self.initial['last_name'] = self.instance.user.last_name
#             self.initial['email'] = self.instance.user.email

#     def clean(self):
#         cleaned_data = super(EmployeeUpdateForm, self).clean()
#         # Custom cleaning logic if needed
#         return cleaned_data

#     def save(self, commit=True):
#         instance = super(EmployeeUpdateForm, self).save(commit=False)
#         if instance.user:
#             instance.user.first_name = self.cleaned_data['first_name']
#             instance.user.last_name = self.cleaned_data['last_name']
#             instance.user.email = self.cleaned_data['email']
#             if commit:
#                 instance.user.save()
#         if commit:
#             instance.save()
#         return instance

# class EmployeeUpdateForm(forms.ModelForm):
#     class Meta:
#         model = Employee
#         exclude = ( 'leave_requests', 'aadhar_image', 'pancard_image', 'profile_picture')  # Exclude these fields from the form

#     # Additional fields from the related User model
#     first_name = forms.CharField(max_length=100, required=False)
#     last_name = forms.CharField(max_length=100, required=False)
#     email = forms.EmailField(max_length=200, required=False)

#     def __init__(self, *args, **kwargs):
#         super(EmployeeUpdateForm, self).__init__(*args, **kwargs)
#         # Set initial values for fields from the related User model if they exist
#         if self.instance.user:
#             self.initial['first_name'] = self.instance.user.first_name
#             self.initial['last_name'] = self.instance.user.last_name
#             self.initial['email'] = self.instance.user.email

#     def clean(self):
#         cleaned_data = super(EmployeeUpdateForm, self).clean()
#         # Custom cleaning logic if needed for fields
#         return cleaned_data

#     def save(self, commit=True):
#         instance = super(EmployeeUpdateForm, self).save(commit=False)
#         # Update associated User model fields if they're included in the form
#         if instance.user and 'first_name' in self.cleaned_data:
#             user = instance.user
#             user.first_name = self.cleaned_data['first_name']
#             user.last_name = self.cleaned_data['last_name']
#             user.email = self.cleaned_data['email']
#             if commit:
#                 user.save()
#         if commit:
#             instance.save()
#         return instance


from django import forms
from django.contrib.auth.models import User
from .models import Employee  # Replace with your actual Employee model

from django import forms
from django.contrib.auth.models import User
from .models import Employee






        


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['company_name', 'company_logic', 'company_intime', 'company_outtime', 'company_logo']
        widgets = {
            'company_logic': forms.Select(choices=Company.WORKING_DAYS_CHOICES),
            'company_intime': forms.TimeInput(attrs={'type': 'time'}),
            'company_outtime': forms.TimeInput(attrs={'type': 'time'}),
        }
        
class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)



class EmployeeCreationForm(forms.Form):
    emp_id = forms.CharField(max_length=100)
    reporting = forms.CharField(max_length = 100)
    email = forms.EmailField(max_length=200)
    email2 = forms.EmailField(max_length=100)
    bank = forms.CharField(max_length = 40)
    title = forms.ChoiceField(choices=Employee.TITLE)
    first_name = forms.CharField(max_length=100)
    middle_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    address = forms.CharField(widget=forms.Textarea)
    salary = forms.IntegerField()
    annual_ctc = forms.IntegerField()
    standard_basic = forms.IntegerField(label='Standard Basic')
    standard_HRA = forms.IntegerField(label='Standard HRA')
    standard_edu_allowance = forms.IntegerField(label='Standard Edu Allowance')
    standard_statutory_bonus = forms.IntegerField(label='Standard Statutory Bonus')
    standard_conveyance_allowance = forms.IntegerField(label='Standard Conveyance Allowance')
    standard_LTA = forms.IntegerField(label='Standard LTA')
    other_allowance = forms.IntegerField(label='Other Allowance')
    nominee = forms.CharField()
    nominee_relation = forms.CharField()
    aadhaar = forms.IntegerField()
    bank_account_no = forms.IntegerField()
    ifsc_code = forms.CharField(max_length=100)
    company = forms.ModelChoiceField(queryset=Company.objects.all())
    pan_no = forms.CharField(max_length=50)
    mobile_no = forms.IntegerField()
    
    emg_mobile_no_1 = forms.IntegerField(label='Emergency Mobile Number 1')
    emg_mobile_no_2 = forms.IntegerField(label='Emergency Mobile Number 2')
    emg_relation_1 = forms.CharField(max_length=100, label='Relation for Emergency Contact 1')
    emg_relation_2 = forms.CharField(max_length=100, label='Relation for Emergency Contact 2')
    designation = forms.CharField(max_length=100)
    loanamount = forms.DecimalField(max_digits=10, decimal_places=2, required=False, label='Loan Amount')
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
    emi = forms.ChoiceField(choices=EMI_CHOICES, label='EMI Choices')
    emi_per_month = forms.DecimalField(max_digits=10, decimal_places=2, required=False, label='EMI per Month')
    current_address = forms.CharField(widget=forms.Textarea)
    blood_group = forms.ChoiceField(choices=Employee.BLOOD_GROUP_CHOICES)
    gender = forms.ChoiceField(choices=Employee.GENDER_CHOICES)
    marital_status = forms.ChoiceField(choices=Employee.MARITAL_STATUS)
    anniversary_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'readonly': 'readonly'}),
        required=False
    )
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    date_of_joining = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    date_of_probation = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    profile_picture = forms.ImageField(label='Profile Picture', required=False)
    CL = forms.IntegerField()
    SL = forms.IntegerField()
    PL = forms.IntegerField()
    UL = forms.IntegerField()
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password']


    def clean(self):
        cleaned_data = super().clean()
        marital_status = cleaned_data.get('marital_status')
        anniversary_date = cleaned_data.get('anniversary_date')

        if marital_status == 'Married' and not anniversary_date:
            self.add_error('anniversary_date', 'Anniversary date is required if married.')

        return cleaned_data

    def save(self, commit=True):
        try:
            company = self.cleaned_data.get('company')
            cintime = company.company_intime if company else None
            couttime = company.company_outtime if company else None

            user = User.objects.create_user(
                username=self.cleaned_data['email'],
                email=self.cleaned_data['email'],
                
                first_name=self.cleaned_data['first_name'],
                
                last_name=self.cleaned_data['last_name'],
                password=self.cleaned_data['password'],
            )

            employee = Employee.objects.create(
                user=user,
                middle_name=self.cleaned_data['middle_name'],
                reporting = self.cleaned_data['reporting'],
                title=self.cleaned_data['title'],
                CL=self.cleaned_data['CL'],
                SL=self.cleaned_data['SL'],
                UL=self.cleaned_data['UL'],
                PL=self.cleaned_data['PL'],
                company=company,
                couttime=couttime,
                cintime=cintime,
                email2 = self.cleaned_data['email2'],
                bank = self.cleaned_data['bank'],
                annual_ctc =self.cleaned_data['annual_ctc'],
                nominee = self.cleaned_data['nominee'],
                nominee_relation = self.cleaned_data['nominee_relation'],
                mobile_no=self.cleaned_data['mobile_no'],
                emg_mobile_no_1=self.cleaned_data['emg_mobile_no_1'],
                emg_mobile_no_2=self.cleaned_data['emg_mobile_no_2'],
                emg_relation_1=self.cleaned_data['emg_relation_1'],
                emg_relation_2=self.cleaned_data['emg_relation_2'],
                marital_status = self.cleaned_data['marital_status'],
                anniversary_date=self.cleaned_data['anniversary_date'],
                aadhaar=self.cleaned_data['aadhaar'],
                bank_account_no=self.cleaned_data['bank_account_no'],
                salary=self.cleaned_data['salary'],
                pan_no=self.cleaned_data['pan_no'],
                ifsc_code=self.cleaned_data['ifsc_code'],
                emp_id=self.cleaned_data['emp_id'],
                designation=self.cleaned_data['designation'],
                address=self.cleaned_data['address'],
                current_address=self.cleaned_data['current_address'],
                blood_group=self.cleaned_data['blood_group'],
                gender=self.cleaned_data['gender'],
                date_of_birth=self.cleaned_data['date_of_birth'],
                date_of_joining=self.cleaned_data['date_of_joining'],
                date_of_probation=self.cleaned_data['date_of_probation'],
                late_min_ava=90,  # Set default value for late_min_ava
                late_time_ava=timedelta(minutes=90),
                standard_basic=self.cleaned_data['standard_basic'],
                standard_HRA=self.cleaned_data['standard_HRA'],
                standard_edu_allowance=self.cleaned_data['standard_edu_allowance'],
                standard_statutory_bonus=self.cleaned_data['standard_statutory_bonus'],
                standard_conveyance_allowance=self.cleaned_data['standard_conveyance_allowance'],
                other_allowance=self.cleaned_data['other_allowance'],
                standard_LTA=self.cleaned_data['standard_LTA'],
                loanamount=self.cleaned_data.get('loanamount'),
                emi=self.cleaned_data.get('emi'),
                emi_per_month=self.cleaned_data.get('emi_per_month'),
            )
            

            profile_picture = self.cleaned_data.get('profile_picture')
            if profile_picture:
                employee.profile_picture = profile_picture
                employee.save()

            return employee, user

        except Exception as e:
            logger.error("Error creating employee or user: %s", e)
            if commit:
                transaction.rollback()
            return None, None


from datetime import datetime
from django.core.exceptions import ValidationError
from .models import Employee 
from django.http import JsonResponse
import json


class HRAttendance(forms.ModelForm):
    intime = forms.TimeField(label='In Time', widget=forms.TimeInput(attrs={'type': 'time'}))
    outtime = forms.TimeField(label='Out Time', required=False, widget=forms.TimeInput(attrs={'type': 'time'}))
    date = forms.DateField(label='Date', widget=forms.DateInput(attrs={'type': 'date'}))
    remark = forms.CharField(label='Remark', required=False, max_length=100)

    class Meta:
        model = Attendance
        fields = ['employee', 'intime', 'outtime', 'date', 'remark']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['employee'].queryset = Employee.objects.all() 

class AttendanceForm(forms.ModelForm):
    intime = forms.TimeField(label='In Time', widget=forms.TimeInput(attrs={'type': 'time'}))
    outtime = forms.TimeField(label='Out Time', required=False, widget=forms.TimeInput(attrs={'type': 'time'}))
    remark = forms.CharField(label='Remark', required=False, max_length=100)
    date = forms.DateField(label='Date', widget=forms.DateInput(attrs={'type': 'date'}))
    

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set the initial value of the date field to the current date
        self.fields['date'].initial = date.today()

    class Meta:
        model = Attendance
        fields = ['intime', 'outtime', 'date', 'remark']

    def clean_intime(self):
        intime = self.cleaned_data.get('intime')
        current_time = datetime.now().time()

        
        
        # Combine the date component of 'current_time' with the 'intime'
        employee_cintime = Employee.objects.values_list('cintime', flat=True).first()
        if isinstance(employee_cintime, datetime):
            employee_cintime = employee_cintime.time()

    # Compare intime with Employee.cintime
    
        
            if intime == current_time:
        # If intime matches current time, check if it's less than employee_cintime
                if intime < employee_cintime:
                    return employee_cintime
                else:
                    return intime
            else:
        # If intime is not current time, set it to current time
                raise forms.ValidationError("Please enter the current time.")
            # Ensure intime is not greater than current time
        
            

        return intime
        

    def clean_outtime(self):
        outtime = self.cleaned_data.get('outtime')

        # Get the current time without the date component
        current_time = datetime.now().time()

        # Ensure out-time is later than the current time
        if outtime and outtime > current_time:
            raise forms.ValidationError("Out time cannot be greater than the current time")

        return outtime

    def clean_date(self):
        date_value = self.cleaned_data.get('date')

        # Ensure the entered date is not in the future and not before today
        # if date_value > date.today():
        #     raise forms.ValidationError("Date cannot be in the future")
        # elif date_value < date.today():
        #     raise forms.ValidationError("Date cannot be in the past")

        return date_value

    def clean(self):
        cleaned_data = super().clean()
        intime = cleaned_data.get('intime')
        outtime = cleaned_data.get('outtime')
        date_value = cleaned_data.get('date')

        # Ensure out-time is later than in-time
        if intime and outtime and outtime <= intime:
            raise forms.ValidationError("Out time must be later than in time")

        # Check if self.instance exists and has an employee attribute
        if self.instance and hasattr(self.instance, 'employee'):
            employee = self.instance.employee
        else:
            # If self.instance does not exist or does not have an employee attribute,
            # try to get the employee from the cleaned data
            employee = cleaned_data.get('employee')

        # Check if attendance for this date and employee already exists
        if employee and Attendance.objects.filter(date=date_value, employee=employee).exists():
            existing_attendance = Attendance.objects.get(date=date_value, employee=employee)
            if existing_attendance.is_locked:
                raise forms.ValidationError("Attendance for this date is already locked.")

        return cleaned_data



from django import forms
from .models import Attendance


        

    




class LeaveRequestForm(forms.ModelForm):
    leave_type = forms.ChoiceField(label='Leave Type', choices=LeaveRequest.LEAVE_CHOICES)
    leaveremark = forms.CharField(label='Remark', max_length=100, required=False)
    date = forms.DateField(label='Date', widget=forms.DateInput(attrs={'type': 'date'}))
    status = forms.CharField(widget=forms.HiddenInput(), initial='Pending')
    
    class Meta:
        model = LeaveRequest
        fields = ['leave_type', 'date', 'leaveremark' ]
        
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set default status to 'Pending' if status is not set
        if 'status' not in self.initial:
            self.initial['status'] = 'Pending'
        # Hide the status field from the form
        self.fields['status'].widget = forms.HiddenInput()
            
    def clean_date(self):
        date = self.cleaned_data['date']
        if date < timezone.now().date():
            raise forms.ValidationError("Date cannot be in the past.")
        return date
        
class WFHODForm(forms.Form):
    employee = forms.ModelChoiceField(queryset=Employee.objects.all(), label='Employee', to_field_name='emp_id')
    date = forms.DateField(label='Date', widget=forms.DateInput(attrs={'type': 'date'}))
    
    WFH = 'WFH'
    OD = 'OD'
    WFHOD_CHOICES = [
        (WFH, 'Work From Home'),
        (OD, 'On Duty'),
    ]
    wfhstatus = forms.ChoiceField(choices=WFHOD_CHOICES, label='Attendance Type', widget=forms.Select(attrs={'class': 'form-control'}))
    
    wfhodremark = forms.CharField(label='Remark', max_length=100)
    remark = forms.CharField(label='Additional Remark', max_length=100, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['employee'].label_from_instance = lambda obj: f"{obj.emp_id} - {obj.user.first_name} {obj.user.last_name}"
        
    
        
class LeaveRequestApprovalForm(forms.ModelForm):
    class Meta:
        model = LeaveRequest
        fields = ['status','hrleaveremark']  # Only include fields relevant for HR approval/rejection
        widgets = {
            'status': forms.Select(choices=LeaveRequest.STATUS_CHOICES),  # Dropdown for status
             # Hidden field for approved_by (auto-filled by view)
        }
        labels = {
            'hrleaveremark': 'HR Leave Remark',
        }



class TimeUpdateForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['employee', 'intime', 'date', 'outtime']
        widgets = {
            'employee': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'intime': forms.TimeInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'outtime': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
        }

    def clean_outtime(self):
        outtime = self.cleaned_data.get('outtime')
        current_time = datetime.now().time()

        

        return outtime




class OutTimeUpdateForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['date', 'intime', 'outtime']
        widgets = {
            'date': forms.DateInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'intime': forms.TimeInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'outtime': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
        }
    
    def clean_outtime(self):
        outtime = self.cleaned_data['outtime']
        utc_now = timezone.now().astimezone(timezone.utc).time()  # Get current UTC time
        
        if outtime >= utc_now:
            raise forms.ValidationError("Out time cannot be in the future or present moment.")
        
        return outtime

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'instance' in kwargs:
            instance = kwargs['instance']
            if instance.date:
                self.fields['date'].widget.attrs['value'] = instance.date.strftime('%Y-%m-%d')
            if instance.intime:
                self.fields['intime'].widget.attrs['value'] = instance.intime.strftime('%H:%M')

    def clean_outtime(self):
        outtime = self.cleaned_data.get('outtime')

        # Get the current time
        current_time = datetime.now().time()

        # Ensure out-time is not greater than the current time
        if outtime and outtime > current_time:
            raise forms.ValidationError("Out time cannot be greater than the current time")

        return outtime


class ProfileUpdateForm(forms.Form):
    old_password = forms.CharField(label='Old Password', widget=forms.PasswordInput)
    new_password = forms.CharField(label='New Password', widget=forms.PasswordInput)
    confirm_password = forms.CharField(label='Confirm New Password', widget=forms.PasswordInput)
    email = forms.EmailField(label='Email', required=True)
    username = forms.CharField(label='Username', max_length=150, required=True)

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")

        if new_password != confirm_password:
            raise forms.ValidationError("New password and confirm password do not match.")
        
        return cleaned_data
    

