# Generated by Django 3.1.2 on 2020-11-09 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('generator', '0005_dataset_date_modified'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dataset',
            name='celery_task_id',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='dataset',
            name='result_file_url',
            field=models.URLField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='schema',
            name='string_character',
            field=models.CharField(choices=[("'", "Single-quote(')"), ('"', 'Double-quote(")'), ('', 'No-quote')], default='"', max_length=1),
        ),
        migrations.AlterField(
            model_name='schemacolumn',
            name='integer_range_from',
            field=models.PositiveSmallIntegerField(blank=True, default=0),
        ),
        migrations.AlterField(
            model_name='schemacolumn',
            name='integer_range_to',
            field=models.PositiveSmallIntegerField(blank=True, default=10),
        ),
        migrations.AlterField(
            model_name='schemacolumn',
            name='text_number_of_sentences',
            field=models.PositiveSmallIntegerField(blank=True, default=1),
        ),
    ]
