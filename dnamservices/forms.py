from django import forms
from django.db.models import fields
from django.forms import ModelForm
from .models import *
from django.contrib.auth.models import User

class SuperviserLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())
    
class ContactForm(forms.ModelForm):
    class Meta:
        model = Contacts
        fields = '__all__'


# client forms

class AddClientForm(forms.ModelForm):
    class Meta:
        model = Client
        exclude = ['delete']
    
class EditClientForm(forms.ModelForm):
    class Meta:
        model = Client
        exclude = ['__all__']
    
class AddSitesForm(forms.ModelForm):
    class Meta:
        model = Sites
        exclude = ['client', 'sunday', 'monday', 'tuesday', 'wednesday', 'thrusday', 'friday', 'saturday', 'remove']
    
class EditSitesForm(forms.ModelForm):
    class Meta:
        model = Sites
        fields = '__all__'
        exclude = ['client', 'sunday', 'monday', 'tuesday', 'wednesday', 'thrusday', 'friday', 'saturday', 'enter']
    
   
class AddSiteWorkingdays(forms.ModelForm):
    class Meta:
        model = Sites
        fields = ['sunday', 'monday', 'tuesday', 'wednesday', 'thrusday', 'friday', 'saturday']

# Invoice Forms
class AddInvoiceInForm(forms.ModelForm):
    class Meta:
        model = InvoiceIn
        exclude = ['delete']

class AddInvoiceOutForm(forms.ModelForm):
    class Meta:
        model = InvoiceOut
        fields = '__all__'
        exclude = ['delete']

class EditInvoiceInForm(forms.ModelForm):
    class Meta:
        model = InvoiceIn
        fields = '__all__'

class EditInvoiceOutForm(forms.ModelForm):
    class Meta:
        model = InvoiceOut
        fields = '__all__'

# Employee Forms
    
class AddEmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['employee_name', 'employee_contact', 'employee_address', 'employee_email']

class EditEmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['employee_name', 'employee_contact', 'employee_address', 'employee_email']

class AddSuperviserAsEmployee(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['employee_user', 'employee_name']

# superviser Forms
class SuperviserRegistrationForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput())
    email = forms.CharField(widget=forms.EmailInput())
    password1 = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = Superviser
        fields = ["superviser_name", "superviser_address"]

# Task Forms
class AddWorkOrderForm(forms.ModelForm):
    class Meta:
        model = WorkOrderTask
        fields = '__all__'
        exclude = ['workorder_user', 'client_name']

class AddComplaintsForm(forms.ModelForm):
    class Meta:
        model = ComplaintTask
        fields = '__all__'
        exclude = ['complaint_user', 'client_name']
    

