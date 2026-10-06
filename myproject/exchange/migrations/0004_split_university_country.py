from django.db import migrations, models


def split_university(value):
    """Split "Name, Country" / "Name (Country)" / "Name - Country" into (name, country)."""
    value = value.strip()
    if value.endswith(")") and "(" in value:
        name, _, country = value[:-1].rpartition("(")
    elif " - " in value:
        name, _, country = value.rpartition(" - ")
    elif "," in value:
        name, _, country = value.rpartition(",")
    else:
        return value, ""
    return name.strip(), country.strip()


def merge_university(name, country):
    return f"{name}, {country}" if country else name


def split_forward(apps, schema_editor):
    ExchangeProgram = apps.get_model("exchange", "ExchangeProgram")
    for program in ExchangeProgram.objects.all():
        program.university, program.country = split_university(program.university)
        program.save(update_fields=["university", "country"])


def split_backward(apps, schema_editor):
    # Lossy: the original separator ("(…)", " - " or ",") is not stored anywhere,
    # so every row comes back in the "Name, Country" form.
    ExchangeProgram = apps.get_model("exchange", "ExchangeProgram")
    for program in ExchangeProgram.objects.all():
        program.university = merge_university(program.university, program.country)
        program.country = ""
        program.save(update_fields=["university", "country"])


class Migration(migrations.Migration):

    dependencies = [
        ("exchange", "0003_exchangeprogram_country"),
    ]

    operations = [
        migrations.RunPython(split_forward, split_backward),
        migrations.AlterField(
            model_name="exchangeprogram",
            name="university",
            field=models.CharField(max_length=200, verbose_name="назва університету"),
        ),
    ]
