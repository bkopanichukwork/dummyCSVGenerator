from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView

from generator.models import Schema


@method_decorator(login_required, name='dispatch')
class SchemaView(ListView):
    template_name = 'schemas.html'
    model = Schema
