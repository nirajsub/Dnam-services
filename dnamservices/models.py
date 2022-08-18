from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import User

class Client(models.Model):
    client_name = models.CharField(max_length=50)
    client_location = models.CharField(max_length=50)
    client_street = models.CharField(max_length=50)
    client_email = models.EmailField(max_length=254)
    client_website = models.CharField(max_length=50, blank=True, null=True)
    delete = models.BooleanField(("delete"), default=False)

    def __str__(self):
        return self.client_name

class Superviser(models.Model):
    superviser_user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    superviser_name = models.CharField(max_length=50)
    superviser_address = models.CharField(max_length=50)
    superviser_contact = models.CharField(max_length=50)
    delete = models.BooleanField(default=False)

    def __str__(self):
        return self.superviser_name

class Employee(models.Model):
    employee_user = models.OneToOneField(Superviser, null=True, blank=True, on_delete=models.CASCADE)
    employee_name = models.CharField(max_length=50)
    employee_contact = models.CharField(max_length=50, null=True, blank=True)
    employee_address = models.CharField(max_length=50, null=True, blank=True)
    employee_email = models.EmailField(max_length=254, null=True, blank=True)

    def __str__(self):
        return str(self.employee_name)

    
clean_task_enable = [

    ("yes","Yes"),
    ("no","No"),
]

class Sites(models.Model):
    site_name = models.CharField(max_length=50)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    site_title = models.CharField(max_length=50)
    address = models.CharField(max_length=50, default="", blank=True)
    suburb = models.CharField(max_length=50, default="", blank=True)
    postcode = models.CharField(max_length=50, default="", blank=True)
    site_contact = models.CharField(max_length=50, default="", blank=True)
    site_attribute = models.CharField(max_length=100, default="", blank=True)
    service = models.CharField(max_length=100, default="", blank=True)
    clean_schedule = models.CharField(max_length=100, default="", blank=True)
    clean_area = models.CharField(max_length=50, default="", blank=True)
    clean_task_enable = models.CharField(default="", max_length=10, choices=clean_task_enable, blank=True)
    cleaner = models.ManyToManyField(Employee, default="", blank=True)
    startdate = models.DateField(auto_now=False, auto_now_add=False, blank=True)
    extra_detail = models.TextField(blank=True)
    sunday = models.IntegerField(default="0", blank=True)
    monday = models.IntegerField(default="0", blank=True)
    tuesday = models.IntegerField(default="0", blank=True)
    wednesday = models.IntegerField(default="0", blank=True)
    thrusday = models.IntegerField(default="0", blank=True)
    friday = models.IntegerField(default="0", blank=True)
    saturday = models.IntegerField(default="0", blank=True)
    enter = models.BooleanField("save")
    remove = models.BooleanField("delete",default=False)

    def __str__(self):
        return self.site_name

class WorkOrderTask(models.Model):
    workorder_user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    client_name = models.ForeignKey(Client, null=True, blank=True, on_delete=models.CASCADE)
    site = models.ForeignKey(Sites, on_delete=models.CASCADE)  
    workorder =  models.CharField(max_length=50)
    workorder_title = models.CharField(max_length=50)
    pricing = models.IntegerField(null=True, blank=True)
    comments = models.CharField(max_length=50, null=True, blank=True,)
    assigned_to = models.ManyToManyField(Employee, null=True, blank=True,)
    completed_by = models.CharField(max_length=50, null=True, blank=True,)
    completion_date = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True,)
    extra_detail = models.TextField(null=True, blank=True)
    show = models.BooleanField(default=False)
    delete = models.BooleanField(default=False)

    def __str__(self):
        return self.workorder

class ComplaintTask(models.Model):
    complaint_user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    client_name = models.ForeignKey(Client, null=True, blank=True, on_delete=models.CASCADE)
    site = models.ForeignKey(Sites, on_delete=models.CASCADE)  
    workorder =  models.CharField(max_length=50)
    pricing = models.IntegerField(null=True, blank=True)
    comments = models.CharField(max_length=50, null=True, blank=True)
    assigned_to = models.ManyToManyField(Employee, null=True, blank=True)
    completed_by = models.CharField(max_length=50, null=True, blank=True)
    completion_date = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True)
    extra_detail = models.TextField(null=True, blank=True)
    show = models.BooleanField(default=False)
    delete = models.BooleanField(default=False)

    def __str__(self):
        return self.workorder

class InvoiceIn(models.Model):
    name = models.CharField(max_length=50)
    in_image = models.FileField(("File"), upload_to="Invoice_in", blank=True, null = True)
    invoice_type = models.CharField(("Type"), max_length=50)
    delete = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class InvoiceOut(models.Model):
    name = models.CharField(max_length=50)
    out_image = models.FileField(("File"), upload_to="Invoice_out", blank=True, null = True)
    invoice_type = models.CharField(("Type"), max_length=50)
    delete = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Contact(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=20)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return 'messege from ' + self.name
    
    class Meta:
        ordering = ['id',]  

    
class Services(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='media/services')
    detail = models.TextField()
    fade = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Career(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='media/career')
    detail = models.TextField()
    role = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Ourteam(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='media/team')
    role = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class AboutUs(models.Model):
    image = models.ImageField(upload_to='media/career')
    detail = models.TextField()

    def __str__(self):
        return self.detail