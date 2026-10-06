from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("exchange", "0002_seed_programs"),
    ]

    operations = [
        migrations.AddField(
            model_name="exchangeprogram",
            name="country",
            field=models.CharField(
                blank=True, default="", max_length=100, verbose_name="країна"
            ),
        ),
    ]
