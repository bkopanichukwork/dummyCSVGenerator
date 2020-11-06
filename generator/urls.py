from django.urls import path

from generator.views import SchemasList, SchemaCreate, SchemaUpdate, SchemaDelete
from django.urls import path
urlpatterns = [
    path('', SchemasList.as_view(), name='schemas-list'),
    path('create/', SchemaCreate.as_view(), name='schema_create'),
    path('update/<int:pk>/', SchemaUpdate.as_view(), name='schema_update'),
    path('delete/<int:pk>/', SchemaDelete.as_view(), name='schema_delete'),
]
