
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import *
from .import views

urlpatterns = [
    # landing pages url
    path('', HomeView, name="home"),
    path('servicedetail/<str:pk>', ServiceDetailView, name="servicedetail"),
    path('aboutus', AboutUsView, name="aboutus"),
    path('services', ServicesView, name="services"),
    path('career', CareerView, name="career"),
    path("supervisor-login/", SuperviserLoginView.as_view(), name="superviser_login"),

    # dashboard url
    path('dashboard/', DashboardView, name="dashboard"),

    # client url
    path('allclients', AllClientView, name="allclients"),
    path('addclients', AddClientView, name="addclients"),
    path('editclients/<str:pk>', EditClientView, name="editclients"),
    path('clientsite/<str:pk>', ClientSitesView, name="clientsites"),
    path('addsite/<str:pk>', AddSitesView, name="addsite"),
    path('editsite/<str:pk>', EditSitesView, name="editsite"),
    path('addworkingdays/<str:pk>', AddWorkingDaysView, name= "addworkingdays"),
    path('sitetasks/<str:pk>', SitesTaskView, name= 'sitetasks'),
    path('deleteclient/<str:pk>/', DeleteClientView, name="deleteclient"),
    path('deleteclientsite/<str:pk>', DeleteClientSite, name="deleteclientsites"),

    # invoice url
    path('invoicein', InvoiceInView, name="invoicein"),
    path('invoiceout', InvoiceOutView, name="invoiceout"),
    path('addinvoicein', AddInvoiceInView, name="addinvoicein"),
    path('addinvoiceout', AddInvoiceOutView, name="addinvoiceout"),
    path('edit-invoice-in/<str:pk>', EditInvoiceInView, name="editinvoicein"),
    path('edit-invoice-out/<str:pk>', EditInvoiceOutView, name="editinvoiceout"),
    path('delete-invoice-in/<str:pk>', DeleteInvoiceIn, name="deleteinvoicein"),
    path('delete-invoice-out/<str:pk>', DeleteInvoiceOut, name="deleteinvoiceout"),

    # employee url
    path('allemployee', AllEmployees, name="allemployee"),
    path('addemployee', AddEmployee, name="addemployee"),
    path('addsuperemployee', AddSuperEmployee, name="addsuperemployee"),
    path('editemployee/<str:pk>', EditEmployeeView, name="editemployee"),
    path('employeetasks/<str:pk>', EmployeeTasks, name = "employeetasks"),
    path('deleteemployee/<str:pk>', DeleteEmployeeView, name="deleteemployee"),

    # superviser url
    path('allsuperviser', AllSuperviserView, name="allsuperviser"),
    path('superviserdetail/<str:pk>', SuperviserDetailView, name="superviserdetail"),
    path('supervisertask/<str:pk>', SuperviserTaskView, name="supervisertask"),
    path("search-superviser/", SuperviserSearchView.as_view(), name="search_superviser"),
    path("superviser-register/", SuperviserRegistrationView.as_view(), name="superviser_register"),

    # Task Url
    path('alltask/', AllTaskView, name='alltask'),
    path('complaints/', ComplaintTaskView, name='complaints'),
    path('workorderupdate/<str:pk>', WorkorderUpdateView, name='workorderupdate'),
    path('complaintsupdate/<str:pk>', ComplaintsUpdateView, name='complaintsupdate'),
    path("add-work-order/", AddWorkOrderView.as_view(), name="add_work_order"),
    path("add-complaints/", AddComplaitsView.as_view(), name="add_complaints"),
    path("deletetask/<str:pk>/", TaskDeleteView, name="deletetask"),
    path("deletecomplaint/<str:pk>/", ComplaintDeleteView, name="deletecomplaint"),

    # search page url
    path("search-site/", SiteSearchView.as_view(), name="search_site"),
    path("search-client/", ClientSearchView.as_view(), name="search_client"),
    path("search-client-site/<str:pk>/", ClientSiteSearchView, name="search_client_site"),
    path("search-invoice-in/", InvoiceInSearchView.as_view(), name="search_invoice_in"),
    path("search-invoice-out/", InvoiceOutSearchView.as_view(), name="search_invoice_out"),
    path("search-employee/", EmployeeSearchView.as_view(), name="search_employee"),
    path("search-alltask/", AllTaskSearchView.as_view(), name="search_alltask"),

    # account settings
    path('change-password/', views.change_password, name='change_password'),

]
if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)
