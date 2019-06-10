from django.conf import settings
from django.db import models
from django.urls import reverse
from hashid_field import HashidAutoField
from datetime import datetime


class Sale(models.Model):
    """
    https://docs.google.com/spreadsheets/d/17Jnhl-UDyuuhNUvVWF_JfVSrQG4Y5rcrJMGT7II5tPM/edit#gid=471490687
    date, FullName, email/contact, attended, outcome, cash_collected, call_notes
    outcome: won, lost, reschedule, cancelled
    """
    id = HashidAutoField(primary_key=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    date = models.DateField(auto_now=False, auto_now_add=False)
    date_modified = models.DateTimeField(auto_now=True)
    # https://docs.djangoproject.com/en/2.2/ref/models/fields/#datetimefield
    full_name_customer = models.CharField(max_length=100)
    email_customer = models.EmailField()
    attended = models.BooleanField()
    
    # https://docs.djangoproject.com/en/2.2/ref/models/fields/#choices
    # Won - Lost - Deposit/Followup - No Show - Rescheduled ?
    WON = 'Won'
    LOST = 'Lost'
    RESCHEDULE = 'Reschedule'
    CANCELLED = 'Cancelled'
    OUTCOME_CHOICES = (
        (WON, 'Won'),
        (LOST, 'Lost'),
        (RESCHEDULE, 'Reschedule'),
        (CANCELLED, 'Cancelled'),
        # add 'Other (temp)'
    )
    outcome = models.CharField(max_length=12, choices=OUTCOME_CHOICES)

    cash_collected = models.PositiveIntegerField(default=0)
    call_notes = models.TextField(blank=True)
    recording_url = models.URLField(blank=True, max_length=300)

    def get_absolute_url(self):
        return reverse('sales:detail', args=[self.id])
    
    def __str__(self):
        return '{} | {} | {}'.format(self.author, datetime.strftime(self.date, "%d %b %Y"), self.full_name_customer)