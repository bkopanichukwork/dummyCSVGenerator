from django.contrib import admin

from generator.models import Schema, CsvSeparator, SchemaColumn, DataSet


@admin.register(Schema)
class SchemaAdmin(admin.ModelAdmin):
    pass


@admin.register(CsvSeparator)
class SchemaAdmin(admin.ModelAdmin):
    pass


@admin.register(SchemaColumn)
class SchemaAdmin(admin.ModelAdmin):
    pass


@admin.register(DataSet)
class DataSetAdmin(admin.ModelAdmin):
    pass
