from django.views import generic, View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
import django_tables2 as tables
from django_tables2.export.views import ExportMixin
from .tables import SimpleTable
from django.shortcuts import redirect
# from dateutil.relativedelta import relativedelta
from django.urls import reverse
from django.utils import timezone
from django.views.generic.dates import MonthArchiveView, YearArchiveView


from .models import Sale
from django.contrib.auth import get_user_model
from django.db.models import Sum, Count
from django.db.models.functions import TruncMonth, TruncDay


User = get_user_model()


class SaleMonthArchiveView(LoginRequiredMixin, MonthArchiveView, ExportMixin, tables.SingleTableView):
    table_pagination = False # for simple solution display summary footer
    date_field = "date"
    allow_future = True # decide later True of False
    allow_empty = True

    table_class = SimpleTable
    template_name = 'sales/home.html'
    login_url = 'login'
    context_object_name = 'latest_sales_list_personal'

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Sale.objects.all()
        else:
            return Sale.objects.filter(author=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_superuser:
            context['overall'] = Sale.objects.filter(date__month=context['month'].month, date__year=context['month'].year).aggregate(Sum('cash_collected'), Count('id'))
            context['calls_attended'] = Sale.objects.filter(date__month=context['month'].month, date__year=context['month'].year, attended=True).aggregate(Count('id'))
            context['calls_show_up_rate'] = '{}%'.format(int(round(context['calls_attended']['id__count'] / context['overall']['id__count'] * 100, 0))) if context['overall']['id__count'] != 0 else 'no data'
            context['enrollments'] = Sale.objects.filter(date__month=context['month'].month, date__year=context['month'].year, outcome='Won').aggregate(Count('id'))
            context['close'] = '{}%'.format(int(round(context['enrollments']['id__count'] / context['calls_attended']['id__count'] * 100, 0))) if context['calls_attended']['id__count'] != 0 else 'no data'
            context['earnings_per_calll'] = '${}'.format(int(round(context['overall']['cash_collected__sum'] / context['calls_attended']['id__count'], 0))) if context['calls_attended']['id__count'] != 0 else 'no data'
            context['comission'] = '${}'.format(int(round(context['overall']['cash_collected__sum'] * 0.1, 0))) if context['overall']['cash_collected__sum'] else 'no data'
        
        else:
            context['overall'] = Sale.objects.filter(author=self.request.user, date__month=context['month'].month, date__year=context['month'].year).aggregate(Sum('cash_collected'), Count('id'))
            context['calls_attended'] = Sale.objects.filter(author=self.request.user, date__month=context['month'].month, date__year=context['month'].year, attended=True).aggregate(Count('id'))
            context['calls_show_up_rate'] = '{}%'.format(int(round(context['calls_attended']['id__count'] / context['overall']['id__count'] * 100, 0))) if context['overall']['id__count'] != 0 else 'no data'
            context['enrollments'] = Sale.objects.filter(author=self.request.user, date__month=context['month'].month, date__year=context['month'].year, outcome='Won').aggregate(Count('id'))
            context['close'] = '{}%'.format(int(round(context['enrollments']['id__count'] / context['calls_attended']['id__count'] * 100, 0))) if context['calls_attended']['id__count'] != 0 else 'no data'
            context['earnings_per_calll'] = '${}'.format(int(round(context['overall']['cash_collected__sum'] / context['calls_attended']['id__count'], 0))) if context['calls_attended']['id__count'] != 0 else 'no data'
            context['comission'] = '${}'.format(int(round(context['overall']['cash_collected__sum'] * 0.1, 0))) if context['overall']['cash_collected__sum'] else 'no data'

        return context


class SummaryYearView(UserPassesTestMixin, YearArchiveView):
    model = Sale
    date_field = "date"
    allow_empty = True
    template_name = 'sales/summary_year.html'

    def test_func(self):
        return self.request.user.is_superuser
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        total_cash_month_based = Sale.objects.filter(date__year=context['year'].year).annotate(month=TruncMonth('date')).values('month').annotate(s=Sum('cash_collected')).values('month', 's').order_by('month')
        enrollments_month_based = Sale.objects.filter(outcome='Won', date__year=context['year'].year).annotate(month=TruncMonth('date')).values('month').annotate(c=Count('id')).values('month', 'c').order_by('month')
        attended_month_based = Sale.objects.filter(attended=True, date__year=context['year'].year).annotate(month=TruncMonth('date')).values('month').annotate(c=Count('id')).values('month', 'c').order_by('month')
        for entry in total_cash_month_based:
            entry.update({
                'enrollments': 0,
                'attended': 0,
                'comission': int(round(entry['s']*0.1,0)),
            })
            for e in enrollments_month_based:
                if entry['month'] == e['month']:
                    entry.update({
                        'enrollments': e['c']
                    })
            for a in attended_month_based:
                if entry['month'] == a['month']:
                    entry.update({
                        'attended': a['c']
                    })
        
        context['total_month_based'] = total_cash_month_based

        context['user_month_based'] = []
        for user in User.objects.all():
            total_month_based = Sale.objects.filter(author=user, date__year=context['year'].year).annotate(month=TruncMonth('date')).values('month').annotate(c=Count('id'), s=Sum('cash_collected')).values('month', 'c', 's')
            calls_attended = Sale.objects.filter(author=user, attended=True, date__year=context['year'].year).annotate(month=TruncMonth('date')).values('month').annotate(c=Count('id')).values('month', 'c')
            calls_won = Sale.objects.filter(author=user, outcome='Won', date__year=context['year'].year).annotate(month=TruncMonth('date')).values('month').annotate(c=Count('id')).values('month', 'c')

            for entry in total_month_based:
                entry.update({
                    'close': 0,
                    'per_call':0,
                    'comission':0
                })
                for a in calls_attended:
                    if entry['month'] == a['month']:
                        entry.update({
                            'per_call': '${}'.format(int(round(entry['s'] / a['c'], 0))) if a['c'] != 0 else 0,
                            'comission': '${}'.format(int(round(entry['s']*0.1, 0))) if a['c'] != 0 else 0,
                        })
                        for d in calls_won:
                            if d['month'] == a['month']:
                                entry.update({
                                    'close': '{}%'.format(int(round(d['c'] / a['c'] * 100, 0))) if entry['c'] != 0 else 0,
                                })

            context['user_month_based'].append({
                'name': user.username,
                'total': total_month_based,
            })
            
            context['month'] = timezone.now() # add in all views?

        return context




class SummaryView(UserPassesTestMixin, MonthArchiveView):
    model = Sale
    date_field = "date"
    template_name = 'sales/summary.html'
    context_object_name = 'summary_month_table'
    login_url = 'login' # delete?
    allow_future = True # decide later True of False
    allow_empty = True

    def test_func(self):
        return self.request.user.is_superuser
        # TODO: change to smth like this: return self.request.user.is_superuser

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['new1'] = []
        for user in User.objects.all():
            # calls_attended = len(Sale.objects.filter(author=user, attended=True, date__gte=context['month'], date__lte=context['month']+relativedelta(months=+1)))
            calls_attended = len(Sale.objects.filter(author=user, attended=True, date__month=context['month'].month, date__year=context['month'].year))
            calls_booked = len(Sale.objects.filter(author=user, date__month=context['month'].month, date__year=context['month'].year))
            total_cash = Sale.objects.filter(author=user, date__month=context['month'].month, date__year=context['month'].year).aggregate(Sum('cash_collected'))['cash_collected__sum']
            # not filtered by month yet
            context['new1'].append({
                'name': user.username,
                'calls booked': calls_booked,
                'calls attended': calls_attended,
                'Call Show up Rate %': int(round(calls_attended / calls_booked * 100, 0)) if calls_booked != 0 else '--',
                'Enrollments': len(Sale.objects.filter(author=user, outcome='Won', date__month=context['month'].month, date__year=context['month'].year)),
                'Close %': '{}%'.format(int(round(len(Sale.objects.filter(author=user, outcome='Won', date__month=context['month'].month, date__year=context['month'].year)) / calls_attended * 100, 0))) if calls_attended != 0 else '--',
                'Total $': total_cash if total_cash else 0,
                'Earnings Per Call': int(round(Sale.objects.filter(author=user, date__month=context['month'].month, date__year=context['month'].year).aggregate(Sum('cash_collected'))['cash_collected__sum'] / calls_attended, 0)) if calls_attended != 0 else 0,
                'Commission': int(round(Sale.objects.filter(author=user, date__month=context['month'].month, date__year=context['month'].year).aggregate(Sum('cash_collected'))['cash_collected__sum'] * 0.1, 0)) if Sale.objects.filter(author=user, date__month=context['month'].month, date__year=context['month'].year).aggregate(Sum('cash_collected'))['cash_collected__sum'] else 0,
                # can extend user model to Commission
            })
        if sum([user['calls booked'] for user in context['new1']]) > 0:
            context['monthly_totals'] = {
                'calls booked': sum([user['calls booked'] for user in context['new1']]),
                'calls attended': sum([user['calls attended'] for user in context['new1']]),
                'Call Show up Rate %': int(round(sum([user['calls attended'] for user in context['new1']]) / sum([user['calls booked'] for user in context['new1']]) * 100, 0)),
                'Enrollments': sum([user['Enrollments'] for user in context['new1']]),
                'Close %': '{}%'.format(int(round(sum([user['Enrollments'] for user in context['new1']]) / sum([user['calls attended'] for user in context['new1']]) * 100, 0))) if sum([user['calls attended'] for user in context['new1']]) > 0 else 0,
                'Total $': '${}'.format(sum([user['Total $'] for user in context['new1']])),
                'Earnings Per Call': '${}'.format(int(round(sum([user['Total $'] for user in context['new1']]) / sum([user['calls attended'] for user in context['new1']]), 0))) if sum([user['calls attended'] for user in context['new1']]) != 0 else 0,
                'Commission': '${}'.format(sum([user['Commission'] for user in context['new1']])),
            }
        
        context['date_based'] = Sale.objects.filter(date__month=context['month'].month, date__year=context['month'].year).annotate(day=TruncDay('date')).values('day').annotate(c=Count('id'), s=Sum('cash_collected')).values('day', 'c', 's').order_by('-day')
        context['date_based_enr'] = Sale.objects.filter(outcome='Won', date__month=context['month'].month, date__year=context['month'].year).annotate(day=TruncDay('date')).values('day').annotate(enr=Count('id')).values('day', 'enr').order_by('-day')
        context['date_based_att'] = Sale.objects.filter(attended=True, date__month=context['month'].month, date__year=context['month'].year).annotate(day=TruncDay('date')).values('day').annotate(att=Count('id')).values('day', 'att').order_by('-day')

        for entry in context['date_based']:
            entry.update({
                'enr': 0
            })
            for d in list(context['date_based_enr']):
                if d['day'] == entry['day']:
                    entry.update({
                        'enr': d['enr']
                    })
        for entry in context['date_based']:
            entry.update({
                'att': 0
            })
            for d in list(context['date_based_att']):
                if d['day'] == entry['day']:
                    entry.update({
                        'att': d['att']
                    })
        
        return context


class DetailView(UserPassesTestMixin, generic.DetailView):
    model = Sale
    template_name = 'sales/detail.html'

    def test_func(self):
        return self.request.user.is_superuser or self.request.user == self.get_object().author

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['month'] = timezone.now()
        return context


class DeleteView(UserPassesTestMixin, generic.DeleteView):
    model = Sale
    template_name = 'sales/delete.html'

    def test_func(self):
        return self.request.user.is_superuser or self.request.user == self.get_object().author

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['month'] = timezone.now()
        return context
    
    def get_success_url(self):
        return reverse('sales:home')




class UpdateView(UserPassesTestMixin, generic.UpdateView):# , LoginRequiredMixin
    model = Sale
    fields = ['date', 'full_name_customer', 'email_customer', 'attended',
        'outcome', 'cash_collected', 'call_notes', 'recording_url']
    template_name = 'sales/edit.html'

    def test_func(self):
        return self.request.user.is_superuser or self.request.user == self.get_object().author
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['month'] = timezone.now()
        
        return context


class HomeView(LoginRequiredMixin, View):
    login_url = 'login'
    def get(self, request):
        year_str = timezone.now().year
        month_str = timezone.now().month
        return redirect('{}/{}/'.format(year_str, month_str))


class SaleCreate(LoginRequiredMixin, generic.edit.CreateView):
    model = Sale
    login_url = 'login'
    fields = ['date', 'full_name_customer', 'email_customer', 'attended',
        'outcome', 'cash_collected', 'call_notes', 'recording_url']
    template_name = 'sales/create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        # form.instance.date = timezone.now()
        return super(SaleCreate, self).form_valid(form)
    
    def get_initial(self):
        return {
            'date': timezone.now()
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['month'] = timezone.now()
        
        return context