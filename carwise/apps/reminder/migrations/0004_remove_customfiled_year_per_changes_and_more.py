# Generated by Django 4.2.9 on 2024-02-19 19:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("reminder", "0003_customfiled_last_date_changed_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="customfiled",
            name="year_per_changes",
        ),
        migrations.AddField(
            model_name="mileage",
            name="timing_belt_filter_updated_date",
            field=models.DateTimeField(null=True),
        ),
    ]
