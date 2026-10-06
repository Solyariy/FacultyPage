from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="ExchangeProgram",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "university",
                    models.CharField(max_length=200, verbose_name="університет"),
                ),
                (
                    "languages",
                    models.CharField(max_length=200, verbose_name="мови навчання"),
                ),
                (
                    "seats",
                    models.CharField(max_length=50, verbose_name="кількість місць"),
                ),
                ("deadline", models.DateField(verbose_name="дедлайн подачі")),
                ("description", models.TextField(verbose_name="опис")),
            ],
            options={
                "verbose_name": "програма обміну",
                "verbose_name_plural": "програми обміну",
                "ordering": ["deadline", "university"],
            },
        ),
    ]
