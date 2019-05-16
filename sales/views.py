from django.shortcuts import render, get_object_or_404
# from django.urls import reverse
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

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

class HomeView(LoginRequiredMixin, generic.ListView):
    template_name = 'sales/home.html'
    context_object_name = 'latest_sales_list_personal'
    login_url = 'login'

    def get_queryset(self):
        """Return the last five modified sales."""
        return Sale.objects.filter(author=self.request.user).order_by('date_modified')[:5]

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