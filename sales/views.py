from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
import django_tables2 as tables

# from django.http import Http404

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

class UpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Sale
    fields = ['date', 'full_name_customer', 'email_customer', 'attended',
        'outcome', 'cash_collected', 'call_notes']
    template_name = 'sales/edit.html'
    login_url = 'login'


class SimpleTable(tables.Table):
    edit = tables.TemplateColumn('Edit', linkify=("sales:edit", {"pk": tables.A("pk")}), orderable=False)
    # id = tables.Column(linkify=("sales:edit", {"pk": tables.A("pk")}))
    # https://github.com/jieter/django-tables2/commit/204a7f23860d178afc8f3aef50512e6bf96f8f6b

    class Meta:
        model = Sale
        attrs = {"class": "table table-bordered table-hover table-sm table-responsive"}
        # https://getbootstrap.com/docs/4.3/content/tables/
        exclude = ('id','author', 'date_modified')# 'id',
    
    # edit = tables.TemplateColumn('<a href="{% url "sales:detail" sale.id %}">Edit</a>', orderable=False)
    

class HomeView(LoginRequiredMixin, tables.SingleTableView):
    table_class = SimpleTable
    template_name = 'sales/home.html'
    login_url = 'login'
    context_object_name = 'latest_sales_list_personal'
    
    def get_queryset(self):
        """
        Return the last five modified sales.
        No slice [:5] here cause django_tables2 conflict.
        """
        return Sale.objects.filter(author=self.request.user).order_by('date_modified')
