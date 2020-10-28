# Generated by Django 3.1.2 on 2020-10-28 17:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('generator', '0003_schema_column_separator'),
    ]

    operations = [
        migrations.CreateModel(
            name='SchemaColumn',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('column_name', models.CharField(max_length=255)),
                ('type', models.PositiveSmallIntegerField(choices=[(1, 'Full name'), (2, 'Integer'), (3, 'Job'), (4, 'Domain name'), (5, 'Phone number'), (6, 'Text'), (7, 'Date'), (8, 'Email'), (10, 'Company name')], default=1)),
                ('text_number_of_sentences', models.PositiveSmallIntegerField(default=1)),
                ('integer_range_from', models.PositiveSmallIntegerField(default=0)),
                ('integer_range_to', models.PositiveSmallIntegerField(default=1)),
                ('schema', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='generator.schema')),
            ],
        ),
    ]