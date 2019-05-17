import django_tables2 as tables
from .models import Sale


class SimpleTable(tables.Table):
    edit = tables.TemplateColumn('Edit', linkify=("sales:edit", {"pk": tables.A("pk")}), orderable=False)
    # can be added verbose_name=''
    # id = tables.Column(linkify=("sales:edit", {"pk": tables.A("pk")}))
    # https://github.com/jieter/django-tables2/commit/204a7f23860d178afc8f3aef50512e6bf96f8f6b

    class Meta:
        model = Sale
        attrs = {"class": "table table-bordered table-hover table-sm"}
        # table-responsive
        # https://getbootstrap.com/docs/4.3/content/tables/
        exclude = ('id','author', 'date_modified')# 'id',
    
    # edit = tables.TemplateColumn('<a href="{% url "sales:detail" sale.id %}">Edit</a>', orderable=False)