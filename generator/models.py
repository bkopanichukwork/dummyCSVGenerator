from django.contrib.auth.models import User
from django.db import models


class CsvSeparator(models.Model):
    separator = models.CharField(max_length=1, unique=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.name} ({self.separator})'


class Schema(models.Model):
    SINGLE_QUOTE = "\'"
    DOUBLE_QUOTE = "\""
    QUOTES = (
        (SINGLE_QUOTE, "Single-quote(\')"),
        (DOUBLE_QUOTE, "Double-quote(\")"),
    )
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    column_separator = models.ForeignKey(CsvSeparator, on_delete=models.CASCADE)
    string_character = models.CharField(max_length=1, choices=QUOTES, default=DOUBLE_QUOTE)
    date_modified = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.name


class SchemaColumn(models.Model):
    FULL_NAME = 1
    INTEGER = 2
    JOB = 3
    DOMAIN_NAME = 4
    PHONE_NUMBER = 5
    TEXT = 6
    DATE = 7
    EMAIL = 8
    COMPANY_NAME = 10
    TYPES = (
        (FULL_NAME, "Full name"),
        (INTEGER, "Integer"),
        (JOB, "Job"),
        (DOMAIN_NAME, "Domain name"),
        (PHONE_NUMBER, "Phone number"),
        (TEXT, "Text"),
        (DATE, "Date"),
        (EMAIL, "Email"),
        (COMPANY_NAME, "Company name"),
    )
    schema = models.ForeignKey(Schema, on_delete=models.CASCADE)
    column_name = models.CharField(max_length=255)
    type = models.PositiveSmallIntegerField(choices=TYPES, default=FULL_NAME)
    text_number_of_sentences = models.PositiveSmallIntegerField(default=1)
    integer_range_from = models.PositiveSmallIntegerField(default=0)
    integer_range_to = models.PositiveSmallIntegerField(default=1)
    order = models.PositiveSmallIntegerField(default=1)

    def __str__(self):
        return f'{self.column_name} column from {self.schema}'


class DataSet(models.Model):
    schema = models.ForeignKey(Schema, on_delete=models.CASCADE)
    row_count = models.IntegerField(default=10)
    celery_task_id = models.CharField(max_length=255)
    result_file_url = models.URLField(max_length=255,blank=True)
    date_modified = models.DateTimeField(auto_now_add=True)
