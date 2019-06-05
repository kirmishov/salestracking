from django.urls import path

from . import views

"""
TODO: id --> hash id
https://github.com/nshafer/django-hashid-field
"""

app_name = 'sales'
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    # ex: sales/2
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    # ex: sales/2/edit/
    path('<int:pk>/edit/', views.UpdateView.as_view(), name='edit'),
    # new | ex: sales/new
    # Example: /2012/08/
    path('<int:year>/<int:month>/',
         views.SaleMonthArchiveView.as_view(month_format='%m'),
         name="archive_month_numeric"),
    path('summary/<int:year>/<int:month>/', views.SummaryView.as_view(month_format='%m'), name='summary'),
    path('summary/<int:year>/', views.SummaryYearView.as_view(), name='summary_year'),
]