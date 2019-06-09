import re
import csv
import django
django.setup()

from sales.models import Sale
from users.models import CustomUser


with open('For import Salestracking - Hananel-June-sample.csv') as f:
        reader = csv.reader(f)
        for row in reader:
            try:
                cash_c = re.findall(r'\d+', row[6])[0]
            except IndexError:
                cash_c = 0
            _, created = Sale.objects.get_or_create(
                # author=row[0],
                author=CustomUser.objects.get(username=row[0]),
                date=row[1],
                full_name_customer=row[2],
                email_customer=row[3],
                attended=True if row[4]=='yes' else False,
                outcome=row[5].title(),
                cash_collected=cash_c,
                call_notes=row[7]
                )