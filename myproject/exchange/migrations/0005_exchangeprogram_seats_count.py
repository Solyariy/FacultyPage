from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("exchange", "0004_split_university_country"),
    ]

    operations = [
        migrations.AddField(
            model_name="exchangeprogram",
            name="seats_count",
            field=models.PositiveIntegerField(
                null=True, verbose_name="кількість місць"
            ),
        ),
    ]
