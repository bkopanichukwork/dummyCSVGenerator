from django.contrib.auth.models import User
from django.db import models


class CsvSeparator(models.Model):
    """Delimiters for csv cells separations"""
    separator = models.CharField(max_length=1, unique=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.name} ({self.separator})'


class Schema(models.Model):
    """
    Data schema that describes structure of a csv file.
    This schema is used for a random csv file generation.
    """
    SINGLE_QUOTE = "\'"
    DOUBLE_QUOTE = "\""
    NO_QUOTE = " "
    QUOTES = (
        (SINGLE_QUOTE, "Single-quote(\')"),
        (DOUBLE_QUOTE, "Double-quote(\")"),
        (NO_QUOTE, "No-quote"),
    )
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    column_separator = models.ForeignKey(CsvSeparator, on_delete=models.CASCADE)
    string_character = models.CharField(max_length=1, choices=QUOTES, default=DOUBLE_QUOTE)
    date_modified = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.name


class SchemaColumn(models.Model):
    """
    Specific column of a csv file data schema.
    Describes type and order of the column in the csv file schema.
    Also stores some additional info for different types
    (integer_range_from, integer_range_to, text_number_of_sentences)
    """
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
    text_number_of_sentences = models.PositiveSmallIntegerField(default=1, blank=True)
    integer_range_from = models.PositiveSmallIntegerField(default=0, blank=True)
    integer_range_to = models.PositiveSmallIntegerField(default=10, blank=True)
    order = models.IntegerField(default=1)

    def __str__(self):
        return f'{self.column_name} column from {self.schema}'


class DataSet(models.Model):
    """
    Randomly generated data set by data schema.
    Saved in result_file_url as a csv file.
    """
    schema = models.ForeignKey(Schema, on_delete=models.CASCADE)
    row_count = models.IntegerField(default=10)
    celery_task_id = models.CharField(max_length=255, blank=True)
    result_file_url = models.URLField(max_length=255, blank=True)
    date_modified = models.DateTimeField(auto_now_add=True)
