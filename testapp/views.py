from django.views.generic import TemplateView
from django_ag_grid.views import BaseAGGridView
from testapp.models import TestModel


class TestView(BaseAGGridView):
    model = TestModel
    column_defs = [
        {'headerName': 'Test', 'field': 'value', 'filter': 'agTextColumnFilter'}
    ]

class IndexView(TemplateView):
    template_name = "index.html"