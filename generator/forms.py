from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Fieldset, Div, HTML, ButtonHolder, Submit
from .custom_layout_object import *
from django.forms import inlineformset_factory, ModelForm

from generator.models import Schema, SchemaColumn


class SchemaForm(ModelForm):
    class Meta:
        model = Schema
        exclude = ('date_modified', 'owner')

    def __init__(self, *args, **kwargs):
        super(SchemaForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-3 create-label'
        self.helper.field_class = 'col-md-9'
        self.helper.layout = Layout(
            Div(
                ButtonHolder(Submit('submit', 'Submit')),
                Field('name'),
                Field('column_separator'),
                Field('string_character'),
                Fieldset('Schema Columns',
                         Formset('schema_columns')),
            )
        )


class SchemaColumnForm(ModelForm):
    class Meta:
        model = SchemaColumn
        exclude = ()


SchemaColumnFormSet = inlineformset_factory(
    Schema, SchemaColumn, form=SchemaColumnForm,
    fields=['type', 'column_name', 'text_number_of_sentences',
            'integer_range_from', 'integer_range_to'], extra=1, can_delete=True
    )
