from django.conf import settings
from django.db import models
from django.urls import reverse

# Create your models here.

class Sale(models.Model):
    """
    https://docs.google.com/spreadsheets/d/17Jnhl-UDyuuhNUvVWF_JfVSrQG4Y5rcrJMGT7II5tPM/edit#gid=471490687
    date, FullName, email/contact, attended, outcome, cash_collected, call_notes
    outcome: won, lost, reschedule, cancelled
    """
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    date = models.DateTimeField(auto_now=False, auto_now_add=False)
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

    cash_collected = models.PositiveIntegerField()
    call_notes = models.TextField()

    """
    def __str__(self):
        return '{}-{}-{}'.format(date_only, full_name_customer, outcome)
    """
    def get_absolute_url(self):
        return reverse('sales:detail', args=[str(self.id)]) # from 'sales:detail'
    
    def __str__(self):
        return '{} | {} | {}'.format(self.author, self.date, self.full_name_customer)