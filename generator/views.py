from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from generator.forms import SchemaForm, SchemaColumnFormSet
from generator.models import Schema


@method_decorator(login_required, name='dispatch')
class SchemasList(ListView):
    def get_queryset(self):
        return Schema.objects.filter(owner=self.request.user)

    template_name = 'generator/schemas.html'
    context_object_name = 'schemas'
    model = Schema


@method_decorator(login_required, name='dispatch')
class SchemaCreate(CreateView):
    model = Schema
    template_name = 'generator/schema_create.html'
    form_class = SchemaForm
    success_url = '/'

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
        return super(SchemaCreate, self).form_valid(form)

    def get_context_data(self, **kwargs):
        data = super(SchemaCreate, self).get_context_data(**kwargs)
        if self.request.POST:
            data['schema_columns'] = SchemaColumnFormSet(self.request.POST)
        else:
            data['schema_columns'] = SchemaColumnFormSet()
        return data


@method_decorator(login_required, name='dispatch')
class SchemaUpdate(UpdateView):
    model = Schema
    template_name = 'generator/schema_create.html'
    form_class = SchemaForm
    success_url = '/'

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
        return super(SchemaUpdate, self).form_valid(form)

    def get_context_data(self, **kwargs):
        data = super(SchemaUpdate, self).get_context_data(**kwargs)
        if self.request.POST:
            data['schema_columns'] = SchemaColumnFormSet(self.request.POST, instance=self.object)
        else:
            data['schema_columns'] = SchemaColumnFormSet(instance=self.object)
        return data


@method_decorator(login_required, name='dispatch')
class SchemaDelete(DeleteView):
    model = Schema
    template_name = 'generator/confirm_delete.html'
    success_url = "/"
