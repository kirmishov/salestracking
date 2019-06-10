import os
import re
import csv
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
django.setup()

from sales.models import Sale
from users.models import CustomUser

outcome_choices = ('Won', 'Lost', 'Reschedule', 'Cancelled')

with open('For import Salestracking - All.csv') as f:
        reader = csv.reader(f)
        for row in reader:
            try:
                cash_c = re.findall(r'\d+', row[6])[0]
            except IndexError:
                cash_c = 0
            _, created = Sale.objects.get_or_create(
                author=CustomUser.objects.get(username=row[0]),
                date=row[1],
                full_name_customer=row[2],
                email_customer=row[3],
                attended=True if row[4]=='yes' else False,
                outcome=row[5].title() if row[5].title() in outcome_choices else 'Reschedule',
                cash_collected=cash_c,
                call_notes=row[7],
                recording_url=row[8]
                )