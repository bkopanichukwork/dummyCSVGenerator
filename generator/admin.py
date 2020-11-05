from django.contrib import admin

from generator.models import Schema, CsvSeparator, SchemaColumn


@admin.register(Schema)
class SchemaAdmin(admin.ModelAdmin):
    pass


@admin.register(CsvSeparator)
class SchemaAdmin(admin.ModelAdmin):
    pass


@admin.register(SchemaColumn)
class SchemaAdmin(admin.ModelAdmin):
    pass
