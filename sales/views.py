from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic, View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
import django_tables2 as tables
from .tables import SimpleTable
from django.http import HttpResponse
from django.shortcuts import redirect

from django.views.generic.dates import MonthArchiveView

from .models import Sale

"""
def index(request):
    latest_sales_list = Sale.objects.order_by('-date_modified')[:5]
    context = {
        'latest_sales_list': latest_sales_list,
    }
    return render(request, 'sales/index.html', context)

def detail(request, sale_id):
    sale = get_object_or_404(Sale, pk=sale_id)
    return render(request, 'sales/detail.html', {'sale': sale})

def edit(request, sale_id):
    sale = get_object_or_404(Sale, pk=sale_id)
    return render(request, 'sales/edit.html', {'sale': sale})
"""

class SummaryView(UserPassesTestMixin, generic.ListView):
    template_name = 'sales/summary.html'
    context_object_name = 'latest_sales_list'
    login_url = 'login'

    def get_queryset(self):
        """Return the last five modified sales."""
        return Sale.objects.order_by('-date_modified')[:5]
    
    def test_func(self):
        return self.request.user.username == 'admin'
        # TODO: change to smth like this: return self.request.user.is_superuser

"""
class HomeView(LoginRequiredMixin, generic.ListView):
    template_name = 'sales/home.html'
    context_object_name = 'latest_sales_list_personal'
    login_url = 'login'

    def get_queryset(self):
        # Return the last five modified sales
        return Sale.objects.filter(author=self.request.user).order_by('date_modified')[:5]
"""

class DetailView(LoginRequiredMixin, generic.DetailView):
    model = Sale
    template_name = 'sales/detail.html'
    login_url = 'login'

    # TODO: add test_func like in UpdateView

class UpdateView(UserPassesTestMixin, generic.UpdateView):# , LoginRequiredMixin
    model = Sale
    fields = ['date', 'full_name_customer', 'email_customer', 'attended',
        'outcome', 'cash_collected', 'call_notes']
    template_name = 'sales/edit.html'
    login_url = 'login'

    def test_func(self):
        return self.request.user.is_superuser or self.request.user == self.get_object().author



# class HomeView(LoginRequiredMixin, tables.SingleTableView):
#     table_class = SimpleTable
#     template_name = 'sales/home.html'
#     login_url = 'login'
#     context_object_name = 'latest_sales_list_personal'
    
#     def get_queryset(self):
#         """
#         Return the last five modified sales.
#         No slice [:5] here cause django_tables2 conflict.
#         """
#         return Sale.objects.filter(author=self.request.user).order_by('date_modified')

class HomeView(LoginRequiredMixin, View):
    login_url = 'login'
    def get(self, request):
        # return HttpResponse("test")
        return redirect('2019/05/') # [hardcoded] TODO: def current_year_month() return 2019/05/
        # How solve problem with new (empty) months?



class SaleMonthArchiveView(LoginRequiredMixin, MonthArchiveView, tables.SingleTableView):
    queryset = Sale.objects.all()
    date_field = "date"
    allow_future = True # can delete
    allow_empty = True

    table_class = SimpleTable
    template_name = 'sales/home.html'
    login_url = 'login'
    context_object_name = 'latest_sales_list_personal'