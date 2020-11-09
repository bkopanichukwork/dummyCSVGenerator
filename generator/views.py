from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from generator.forms import SchemaForm, SchemaColumnFormSet
from generator.models import Schema, DataSet

from generator.services import create_random_dataset, \
                               process_schema_form, \
                               check_user_schema_permission


@login_required
def generate_dataset(request, *args, **kwargs):
    """
    Service that generates new dataset by given data schema and rows count
    """
    if request.POST:
        schema_id = request.POST.get("schema")
        row_count = int(request.POST.get("row_count"))
        create_random_dataset(schema_id=schema_id,
                              row_count=row_count)
        return redirect('datasets_list', schema=schema_id)
    else:
        raise Http404()


@method_decorator(login_required, name='dispatch')
class SchemasList(ListView):
    template_name = 'generator/schemas.html'
    context_object_name = 'schemas'
    model = Schema

    def get_queryset(self):
        return Schema.objects.filter(owner=self.request.user)


@method_decorator(login_required, name='dispatch')
class DataSetsList(ListView):
    template_name = 'generator/datasets.html'
    context_object_name = 'datasets'
    model = Schema

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["schema"] = self.kwargs['schema']
        return context

    def get_queryset(self):
        schema = self.kwargs['schema']
        check_user_schema_permission(schema, self.request.user)
        return DataSet.objects.filter(schema=schema)


@method_decorator(login_required, name='dispatch')
class SchemaCreate(CreateView):
    model = Schema
    template_name = 'generator/schema_create.html'
    form_class = SchemaForm
    success_url = '/'

    def form_valid(self, form):
        context = self.get_context_data()
        schema_columns = context['schema_columns']
        process_schema_form(form, schema_columns, self.request.user)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
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

    def get_object(self, queryset=None):
        schema = super(SchemaUpdate, self).get_object()
        check_user_schema_permission(schema.pk, self.request.user)
        return schema

    def form_valid(self, form):
        context = self.get_context_data()
        schema_columns = context['schema_columns']
        process_schema_form(form, schema_columns, self.request.user)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
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

    def get_object(self, queryset=None):
        schema = super(SchemaDelete, self).get_object()
        check_user_schema_permission(schema.pk, self.request.user)
        return schema
