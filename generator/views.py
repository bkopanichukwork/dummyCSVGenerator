from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView

from generator.models import Schema


@method_decorator(login_required, name='dispatch')
class SchemasView(ListView):
    def get_queryset(self):
        return Schema.objects.filter(owner=self.request.user)

    template_name = 'schemas.html'
    context_object_name = 'schemas'
    model = Schema
