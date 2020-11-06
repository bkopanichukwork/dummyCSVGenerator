from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView

from generator.forms import SchemaForm, SchemaColumnFormSet
from generator.models import Schema


@method_decorator(login_required, name='dispatch')
class SchemasListView(ListView):
    def get_queryset(self):
        return Schema.objects.filter(owner=self.request.user)

    template_name = 'generator/schemas.html'
    context_object_name = 'schemas'
    model = Schema


@method_decorator(login_required, name='dispatch')
class SchemaCreateView(CreateView):
    model = Schema
    template_name = 'generator/schema_create.html'
    form_class = SchemaForm
    success_url = '/'

    def get_context_data(self, **kwargs):
        data = super(SchemaCreateView, self).get_context_data(**kwargs)
        if self.request.POST:
            data['schema_columns'] = SchemaColumnFormSet(self.request.POST)
        else:
            data['schema_columns'] = SchemaColumnFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        schema_columns = context['schema_columns']
        with transaction.atomic():
            form.instance.owner = self.request.user
            form.instance.date_modified = datetime.now()
            self.object = form.save()
            if schema_columns.is_valid():
                schema_columns.instance = self.object
                schema_columns.save()
        return super(SchemaCreateView, self).form_valid(form)
