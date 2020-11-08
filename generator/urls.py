from django.urls import path

from generator.views import SchemasList, SchemaCreate, \
                            SchemaUpdate, SchemaDelete, \
                            DataSetsList, generate_dataset


urlpatterns = [
    path('', SchemasList.as_view(), name='schemas_list'),
    path('create/', SchemaCreate.as_view(), name='schema_create'),
    path('update/<int:pk>/', SchemaUpdate.as_view(), name='schema_update'),
    path('delete/<int:pk>/', SchemaDelete.as_view(), name='schema_delete'),
    path('datasets/<int:schema>/', DataSetsList.as_view(), name='datasets_list'),
    path('datasets/<int:schema>/generate/', generate_dataset, name='generate_dataset'),
]
