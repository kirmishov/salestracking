import django_tables2 as tables
from .models import Sale
from django.utils.safestring import mark_safe
from django.utils.html import escape, format_html


class SimpleTable(tables.Table):
    edit = tables.TemplateColumn('Edit', linkify=("sales:edit", {"pk": tables.A("pk")}), orderable=False, exclude_from_export=True)
    recording_url = tables.Column(default='')
    full_name_customer = tables.Column(linkify=("sales:detail", {"pk": tables.A("pk")}))
    # call_notes = TruncatedTextColumn(accessor=tables.A('Call_notes'))
    # '<a href="{{record.recording_url}}">Link</a>'

    # can be added verbose_name=''
    # id = tables.Column(linkify=("sales:edit", {"pk": tables.A("pk")}))
    # https://github.com/jieter/django-tables2/commit/204a7f23860d178afc8f3aef50512e6bf96f8f6b
    

    """
    Method 1 for display summary
    """
    # cash_collected = tables.Column(
    #     footer=lambda table: sum(x.cash_collected for x in table.data)
    # )

    """
    If needed basic cell conditional formatting
    """
    # def render_outcome(self, value, column):
    #     if value=='Won':
    #         # column.attrs = {'td': {'bgcolor': 'lightgreen'}}
    #         column.attrs = {'td': {'class': 'table-success'}}
    #     else:
    #         column.attrs = {'td': {}}
    #     return value

    class Meta:
        model = Sale
        row_attrs = {
            'data-outcome': lambda record: record.outcome
        }
        attrs = {"class": "table table-bordered table-hover table-sm"}
        # table-responsive
        # https://getbootstrap.com/docs/4.3/content/tables/
        exclude = ('id', 'date_modified')
    
    def before_render(self, request):
        if not request.user.is_superuser:
            self.columns.hide('author')
    
    def render_recording_url(self, value):
        return format_html(
            '<a href="{url}">Link</a>',
            url=mark_safe(value)
        )

    def render_call_notes(self, value):
        if len(value) > 102:
            return value[0:99] + '...'
        return str(value)

    def value_call_notes(self, value):
        return value
    
    def value_recording_url(self, value):
        return value