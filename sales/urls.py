from django.urls import path

from . import views


app_name = 'sales'
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('<pk>/', views.DetailView.as_view(), name='detail'),
    path('<pk>/edit/', views.UpdateView.as_view(), name='edit'),
    path('<pk>/delete/', views.DeleteView.as_view(), name='delete'),
    path('<int:year>/<int:month>/',
         views.SaleMonthArchiveView.as_view(month_format='%m'),
         name="archive_month_numeric"),
    path('summary/<int:year>/<int:month>/', views.SummaryView.as_view(month_format='%m'), name='summary'),
    path('summary/<int:year>/', views.SummaryYearView.as_view(), name='summary_year'),
]