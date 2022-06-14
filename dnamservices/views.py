from django.shortcuts import render
from django.shortcuts import render, redirect
from django.views.generic import View, CreateView
from django.contrib.auth.models import User
from django.urls import reverse_lazy, reverse
from django.http import HttpResponse
from django.views.generic import TemplateView, FormView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.core.paginator import Paginator
from django.db.models import Q

from .forms import *
from .models import *

from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages


# account settings
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'dnam/dashboard/users/change_password.html', {
        'form': form
    })


# Landing pages view
def HomeView(request):
    template_name = "dnam/landingpages/home.html"
    service = Services.objects.all().order_by('-id')[0:3]
    form = ContactForm()
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect("home")
    context = {
        'service':service
    }
    return render(request, template_name, context)

def AboutUsView(request):
    template_name = "dnam/landingpages/aboutus.html"
    return render(request, template_name)

def ServicesView(request):
    template_name = "dnam/landingpages/services.html"
    service = Services.objects.all().order_by('-id')
    context = {
        'service':service
    }
    return render(request, template_name, context)

def ServiceDetailView(request, pk):
    template_name = "dnam/landingpages/servicedetail.html"
    service = Services.objects.get(id=pk)
    context = {
        'service':service
    }
    return render(request, template_name, context)

class SuperviserLoginView(FormView):
    template_name = "dnam/landingpages/superviserlogin.html"
    form_class = SuperviserLoginForm
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        uname = form.cleaned_data.get("username")
        pword = form.cleaned_data["password"]
        usr = authenticate(username=uname, password=pword)
        if usr is not None:
            if usr is not None and Superviser.objects.filter(superviser_user=usr).exists():
                login(self.request, usr)
            else:
                error_message = ("Invalid Username")
                return render(self.request, self.template_name, {'error_message':error_message})
        else:
            error_message = ("Invalid Username or password")
            return render(self.request, self.template_name, {'error_message':error_message})
        return super().form_valid(form)
    
# Dashboard view (login is required)
@login_required()
def DashboardView(request):
    template_name = "dnam/dashboard/dashboard/dashboard.html" 
    return render(request, template_name)


class SiteSearchView(LoginRequiredMixin, TemplateView):
    template_name = "dnam/dashboard/search/search_sites.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        kw = self.request.GET.get("keyword")
        results = Sites.objects.filter(
            Q(site_name__icontains=kw) | Q(site_title__icontains=kw) | Q(site_attribute__icontains=kw))
        paginator = Paginator(results, 100)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {
            'results':results,
            'page_obj':page_obj,
        }
        return context
    

# Clinet views
@login_required()
def AllClientView(request):
    template_name = "dnam/dashboard/clients/allclient.html"
    client = Client.objects.all()
    context = {
        'client':client
    }
    return render(request, template_name, context)

@login_required()
def AddClientView(request):
    template_name = "dnam/dashboard/clients/addclient.html"
    form = AddClientForm()
    if request.method == "POST":
        form = AddClientForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect ("allclients")
    context = {
        'form':form,
    }
    return render(request, template_name, context)

@login_required()
def EditClientView(request, pk):
    template_name = "dnam/dashboard/clients/editclient.html"
    client = Client.objects.get(id=pk)
    form = EditClientForm(instance=client)
    if request.method == "POST":
        form = EditClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
        return redirect ("allclients")
    context = {
        'form':form,
        'client':client
    }
    return render(request, template_name, context)

@login_required()
def ClientSitesView(request, pk):
    template_name = "dnam/dashboard/clients/clientsites.html"
    client = Client.objects.get(id=pk)
    site = Sites.objects.all().order_by('-id')
    paginator = Paginator(site, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'client':client,
        'page_obj':page_obj,
    }
    return render(request, template_name, context)

def ClientSiteSearchView(request, pk):
    template_name = "dnam/dashboard/search/search_client_site.html"
    client = Client.objects.get(id=pk)
    kw = request.GET.get("keyword")
    results = Sites.objects.filter(Q(site_name__icontains=kw) | Q(site_title__icontains=kw) | Q(site_attribute__icontains=kw))
    paginator = Paginator(results, 100)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'results':results,
        'client':client,
        'page_obj':page_obj
    }
    return render(request, template_name, context)

class ClientSearchView(TemplateView):
    template_name = "dnam/dashboard/search/search_client.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        kw = self.request.GET.get("keyword")
        results = Client.objects.filter(
            Q(client_name__icontains=kw))
        context = {
            'results':results,
        }
        return context

@login_required()
def AddSitesView(request, pk):
    template_name = "dnam/dashboard/clients/addsites.html"
    clientid = Client.objects.get(id=pk)
    site, created = Sites.objects.get_or_create(client=clientid, enter=False)
    employee = Employee.objects.all()
    form = AddSitesForm(instance=site)
    if request.method == "POST":
        form = AddSitesForm(request.POST, instance=site)
        if form.is_valid():
            form.save()
        else:
            return HttpResponse("not saved")
        return redirect("allclients")
    context = {
        'site':site,
        'clientid':clientid,
        'form':form,
        'employee':employee,
    }
    return render(request, template_name, context)    

@login_required()
def EditSitesView(request, pk):
    template_name = "dnam/dashboard/clients/editsites.html"
    site = Sites.objects.get(id=pk)
    employee = Employee.objects.all()
    form = EditSitesForm(instance=site)
    if request.method == "POST":
        form = EditSitesForm(request.POST, instance=site)
        if form.is_valid():
            form.save()
        else:
            return HttpResponse("not saved")
        return redirect("allclients")
    context = {
        'site':site,
        'form':form,
        'employee':employee,
    }
    return render(request, template_name, context)

@login_required()
def AddWorkingDaysView(request, pk):
    template_name = "dnam/dashboard/clients/addworkingdays.html"
    site = Sites.objects.get(id=pk)
    form = AddSiteWorkingdays(instance=site)
    if request.method == "POST":
        form = AddSiteWorkingdays(request.POST, instance=site)
        if form.is_valid():
            form.save()
        return redirect("allclients")
    context = {
        'site':site,
        'form':form
    }
    return render(request, template_name, context)

@login_required()
def SitesTaskView(request, pk):
    template_name = "dnam/dashboard/clients/sitetasks.html"
    site = Sites.objects.get(id=pk)
    context = {
        'site':site
    }
    return render(request, template_name, context)

def DeleteSiteView(request, pk):
    template_name = "dnam/dashboard/clients/deletesite.html"
    sitedelete = Sites.objects.get(id=pk)
    if request.method=='POST':
        sitedelete.delete()
        return redirect('allclients')
    context = {'sitedelete':sitedelete}
    return render(request, template_name, context)
# Invoice Views

@login_required()
def InvoiceInView(request):
    template_name = "dnam/dashboard/invoices/invoicein.html"
    invoicein = InvoiceIn.objects.all().order_by("-id")
    paginator = Paginator(invoicein, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'invoicein':invoicein,
        'page_obj':page_obj,
    }
    return render(request, template_name, context)

class InvoiceInSearchView(TemplateView):
    template_name = "dnam/dashboard/search/search_invoice_in.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        kw = self.request.GET.get("keyword")
        results = InvoiceIn.objects.filter(
            Q(name__icontains=kw))
        paginator = Paginator(results, 100)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
            'results':results,
            'page_obj':page_obj
        }
        return context

class InvoiceOutSearchView(TemplateView):
    template_name = "dnam/dashboard/search/search_invoice_out.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        kw = self.request.GET.get("keyword")
        results = InvoiceOut.objects.filter(
            Q(name__icontains=kw))
        paginator = Paginator(results, 100)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
            'results':results,
            'page_obj':page_obj
        }
        return context

@login_required()
def InvoiceOutView(request):
    template_name = "dnam/dashboard/invoices/invoiceout.html"
    invoiceout = InvoiceOut.objects.all().order_by("-id")
    paginator = Paginator(invoiceout, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'invoiceout':invoiceout,
        'page_obj':page_obj,
    }
    return render(request, template_name, context)

@login_required()
def AddInvoiceInView(request):
    template_name = "dnam/dashboard/invoices/addinvoicein.html"
    form = AddInvoiceInForm()
    if request.method == "POST":
        form = AddInvoiceInForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        else:
            return HttpResponse("unsupported files")
        return redirect('invoicein')
    context = {
        'form':form
    }
    return render(request, template_name, context)

@login_required()
def EditInvoiceInView(request, pk):
    template_name = "dnam/dashboard/invoices/editinvoicein.html"
    invoice = InvoiceIn.objects.get(id=pk)
    form = EditInvoiceInForm(instance=invoice)
    if request.method == "POST":
        form = EditInvoiceInForm(request.POST, request.FILES, instance=invoice)
        if form.is_valid():
            form.save()
        else:
            error = "invalid form"
            return render(request, template_name, {'error':error})
        return redirect('invoicein')
    context = {
        'form':form,
        'invoice':invoice
    }
    return render(request, template_name, context)

@login_required()
def EditInvoiceOutView(request, pk):
    template_name = "dnam/dashboard/invoices/editinvoiceout.html"
    invoice = InvoiceOut.objects.get(id=pk)
    form = EditInvoiceOutForm(instance=invoice)
    if request.method == "POST":
        form = EditInvoiceOutForm(request.POST, request.FILES, instance=invoice)
        if form.is_valid():
            form.save()
        else:
            error = "invalid form"
            return render(request, template_name, {'error':error})
        return redirect('invoiceout')
    context = {
        'form':form,
        'invoice':invoice,
    }
    return render(request, template_name, context)

@login_required()
def AddInvoiceOutView(request):
    template_name = "dnam/dashboard/invoices/addinvoiceout.html"
    form = AddInvoiceOutForm()
    if request.method == "POST":
        form = AddInvoiceOutForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        else:
            return HttpResponse("unsupported files")
        return redirect('invoiceout')
    context = {
        'form':form
    }
    return render(request, template_name, context)


# employee View

@login_required()
def AllEmployees(request):
    template_name = "dnam/dashboard/employees/allemployee.html"    
    employee = Employee.objects.all()
    context = {
        'employee':employee
    }
    return render(request, template_name, context)

class EmployeeSearchView(TemplateView):
    template_name = "dnam/dashboard/search/search_employee.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        kw = self.request.GET.get("keyword")
        results = Employee.objects.filter(
            Q(employee_name__icontains=kw) | Q(employee_email__icontains=kw))
        context = {
            'results':results,
        }
        return context

@login_required()
def AddEmployee(request):
    template_name = "dnam/dashboard/employees/addemployee.html"
    form = AddEmployeeForm()
    if request.method == "POST":
        form = AddEmployeeForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect("allemployee")
    context = {
        'form':form,
    }
    return render(request, template_name, context)

@login_required()
def AddSuperEmployee(request):
    template_name = "dnam/dashboard/employees/addsuperemployee.html"

    form = AddSuperviserAsEmployee()
    if request.method=="POST":
        form = AddSuperviserAsEmployee(request.POST)
        if form.is_valid():
            form.save()
        return redirect('allemployee')
    context = {
        'form':form
    }
    return render(request, template_name, context)

@login_required()
def EditEmployeeView(request, pk):
    template_name = "dnam/dashboard/employees/editemployee.html"
    employee = Employee.objects.get(id=pk)
    form = EditEmployeeForm(instance=employee)
    
    if request.method=="POST":
        form = EditEmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
        return redirect("allemployee")
    
    context = {
        'form':form,
        'employee':employee
    }
    return render(request, template_name, context)

def DeleteEmployeeView(request, pk):
    template_name = "dnam/dashboard/employees/deleteemployee.html"
    employeedelete = Employee.objects.get(id=pk)
    if request.method=='POST':
        employeedelete.delete()
        return redirect('allemployee')
    context = {'employeedelete':employeedelete}
    return render(request, template_name, context)

@login_required()
def EmployeeTasks(request, pk):
    template_name = "dnam/dashboard/employees/employeetask.html"
    employee = Employee.objects.get(id=pk)
    workorder = WorkOrderTask.objects.all()
    complaint = ComplaintTask.objects.all()
    paginator = Paginator(workorder, 5)
    paginator2 = Paginator(complaint, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    page_obj2 = paginator2.get_page(page_number)

    context = {
        'employee':employee,
        'workorder':workorder,
        'complaint':complaint,
        'page_obj':page_obj,
        'page_obj2':page_obj2,
    }
    return render(request, template_name, context)


# Superviser View

@login_required()
def AllSuperviserView(request):
    template_name = "dnam/dashboard/superviser/allsuperviser.html"   
    user = Superviser.objects.all()
    context = {
        'user':user
    }
    return render(request, template_name, context)

class SuperviserSearchView(TemplateView):
    template_name = "dnam/dashboard/search/search_superviser.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        kw = self.request.GET.get("keyword")
        results = Superviser.objects.filter(
            Q(superviser_name__icontains=kw))
        context = {
            'results':results,
        }
        return context

@login_required()
def SuperviserDetailView(request, pk):
    template_name = "dnam/dashboard/superviser/superviserdetail.html"
    superviser = User.objects.get(id=pk)
    context = {
        'superviser':superviser
    }
    return render(request, template_name, context)

@login_required()
def SuperviserTaskView(request, pk):
    template_name = "dnam/dashboard/superviser/supervisertask.html"
    superviser = Superviser.objects.get(id=pk)
    workorder = WorkOrderTask.objects.all()
    complaint = ComplaintTask.objects.all()
    paginator = Paginator(workorder, 5)
    paginator2 = Paginator(complaint, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    page_obj2 = paginator.get_page(page_number)
    context = {
        'superviser':superviser,
        'workorder':workorder,
        'complaint':complaint,
        'page_obj':page_obj,
        'page_obj2':page_obj2,
    }
    return render(request, template_name, context)

class SuperviserRegistrationView(LoginRequiredMixin, CreateView):
    template_name = "dnam/dashboard/accounts/superviser_register.html"
    form_class = SuperviserRegistrationForm
    success_url = reverse_lazy("allsuperviser")
    def form_valid(self, form):
        username = form.cleaned_data.get("username")
        password1 = form.cleaned_data.get("password1")
        password2 = form.cleaned_data.get("password2")
        email = form.cleaned_data.get("email")
        if User.objects.filter(username=username).exists():
            error = ("Sorry! Superviser with this username already exists.")
            return render(self.request, self.template_name, {'error':error})
        if User.objects.filter(email=email).exists():
            error1= ("Sorry! Superviser with this email already exists. please try new email.")
            return render(self.request, self.template_name, {'error1':error1})
        if password1 == password2:
            user = User.objects.create_user(username, email, password1, is_staff=True)
            form.instance.superviser_user = user
        else:
            error2= ("Password didn't match")
            return render(self.request, self.template_name, {'error2':error2})
        return super().form_valid(form)

    def get_success_url(self):
        if "next" in self.request.GET:
            next_url = self.request.GET.get("next")
            return next_url
        else:
            return self.success_url

# Task Views


@login_required()
def AllTaskView(request):
    template_name = "dnam/dashboard/task/alltask.html"
    workordertask = WorkOrderTask.objects.all().order_by('id')
    complainttask = ComplaintTask.objects.all().order_by("-id")
    paginator = Paginator(workordertask, 5)
    paginator2 = Paginator(complainttask, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    page_obj2 = paginator2.get_page(page_number)
    context = {
        'workordertask':workordertask,
        'complainttask':complainttask,
        'page_obj':page_obj,
        'page_obj2':page_obj2,
    }
    return render(request, template_name, context)

class AllTaskSearchView(LoginRequiredMixin, TemplateView):
    template_name = "dnam/dashboard/search/search_task.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        kw = self.request.GET.get("keyword")
        results = WorkOrderTask.objects.filter(
            Q(workorder__icontains=kw) | Q(comments__icontains=kw) | Q(extra_detail__icontains=kw))
        results2 = ComplaintTask.objects.filter(
            Q(workorder__icontains=kw) | Q(comments__icontains=kw) | Q(extra_detail__icontains=kw))
        context = {
            'results':results,
            'results2':results2,
        }
        return context

class AddWorkOrderView(LoginRequiredMixin, CreateView):
    template_name = 'dnam/dashboard/task/addworkorder.html'
    model = WorkOrderTask
    form_class = AddWorkOrderForm
    success_url = reverse_lazy('alltask')
    def form_valid(self, form):
        form.instance.workorder_user = self.request.user
        return super().form_valid(form)

@login_required()
def WorkorderUpdateView(request, pk):
    template_name = 'dnam/dashboard/task/updateworkorder.html'

    workordertask = WorkOrderTask.objects.get(id=pk)
    form = AddWorkOrderForm(instance=workordertask)
    if request.method == "POST":
        form = AddWorkOrderForm(request.POST, instance=workordertask)
        if form.is_valid():
            form.save()
        return redirect("alltask")
    context = {
        'workordertask':workordertask,
        'form':form
    }
    return render(request, template_name, context)

@login_required()
def ComplaintTaskView(request):
    template_name = "dnam/dashboard/task/complainttask.html"
    complainttask = ComplaintTask.objects.all()

    context = {
        'complainttask':complainttask,
    }
    return render(request, template_name, context)

class AddComplaitsView(LoginRequiredMixin, CreateView):
    template_name = 'dnam/dashboard/task/addcomplaint.html'
    model = ComplaintTask
    form_class = AddComplaintsForm

    success_url = reverse_lazy('alltask')

    def form_valid(self, form):
        form.instance.complaint_user = self.request.user
        return super().form_valid(form)

@login_required()
def ComplaintsUpdateView(request, pk):
    template_name = 'dnam/dashboard/task/updatecomplaints.html'

    complaintstask = ComplaintTask.objects.get(id=pk)
    form = AddComplaintsForm(instance=complaintstask)
    if request.method == "POST":
        form = AddComplaintsForm(request.POST, instance=complaintstask)
        if form.is_valid():
            form.save()
        return redirect("alltask")
    context = {
        'complaintstask':complaintstask,
       'form':form
    }
    return render(request, template_name, context)
