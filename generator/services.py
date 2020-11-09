import csv
import os
from typing import Union

from celery import shared_task
from celery_progress.backend import ProgressRecorder
from faker import Faker

from generator.models import Schema, DataSet, SchemaColumn
from django.conf import settings


def create_random_dataset(schema_id: int, row_count: int) -> None:
    """
    Creates task for generating a new csv file with random data
    using specific data schema.
        Parameters:
            schema_id (int): id of using schema in database
            row_count (int): count of rows in new csv file
    """
    try:
        schema = Schema.objects.get(pk=int(schema_id))
    except Schema.DoesNotExist:
        return None

    ds = DataSet.objects.create(schema=schema,
                                row_count=row_count)

    task = _generate_random_csv_file.delay(schema_id, row_count, ds.pk)
    ds.task_id = task.task_id
    ds.save()


@shared_task(bind=True)
def _generate_random_csv_file(self, schema_id: int, row_count: int, dataset_id: int) -> None:
    """
    Generates new csv file with random data using specific data schema
        Parameters:
            schema_id (int): id of using schema in database
            row_count (int): count of rows in new csv file
            dataset_id (int): id of dataset in database
    """
    schema = Schema.objects.get(pk=schema_id)
    columns = list(SchemaColumn.objects.filter(schema=schema))

    file_name = f"schema_{schema.name}_data_set_{dataset_id}.csv"
    new_csv = os.path.join(settings.MEDIA_ROOT, file_name)

    with open(new_csv, 'w', newline='') as file:
        csv_writer = csv.writer(file,
                                delimiter=schema.column_separator.separator,
                                quotechar=schema.string_character,
                                quoting=csv.QUOTE_NONNUMERIC)
        # generate header
        csv_writer.writerow([col.column_name for col in columns])
        # generate all rows
        for row in range(row_count):
            csv_writer.writerow([_generate_random_value_of_cell(col)
                                 for col in columns])

    dataset = DataSet.objects.get(pk=dataset_id)
    dataset.result_file_url = os.path.join(settings.MEDIA_URL, file_name)
    dataset.save()

    return None


def _generate_random_value_of_cell(cell: SchemaColumn) -> Union[str, int]:
    """ Returns random value based on cell type"""
    fake = Faker()
    if cell.type == cell.FULL_NAME:
        return fake.name()
    if cell.type == cell.EMAIL:
        return fake.email()
    if cell.type == cell.DOMAIN_NAME:
        return fake.domain_name()
    if cell.type == cell.COMPANY_NAME:
        return fake.company()
    if cell.type == cell.TEXT:
        sentences = fake.sentences(cell.text_number_of_sentences)
        return ''.join(sentences)
    if cell.type == cell.JOB:
        return fake.job().replace(',', '')
    if cell.type == cell.INTEGER:
        return fake.random_int(min=cell.integer_range_from,
                               max=cell.integer_range_to)
    if cell.type == cell.DATE:
        return fake.date()
    if cell.type == cell.PHONE_NUMBER:
        return fake.phone_number()
