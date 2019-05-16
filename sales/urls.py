from django.urls import path

from . import views

"""
TODO: id --> hash id
https://github.com/nshafer/django-hashid-field
"""

app_name = 'sales'
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    # ex: /sales/summary
    path('summary/', views.SummaryView.as_view(), name='summary'),
    # ex: sales/2
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    # ex: sales/2/edit/
    path('<int:pk>/edit/', views.UpdateView.as_view(), name='edit'),
    # new | ex: sales/new
]