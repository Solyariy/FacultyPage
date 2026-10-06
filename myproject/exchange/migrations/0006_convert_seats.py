import re

from django.db import migrations


def parse_seats(value):
    """ "5" -> 5, "2 місця" -> 2, "до 4" -> 4 (upper bound, see ANSWERS.md)."""
    match = re.search(r"\d+", value)
    if match is None:
        raise ValueError(f"Cannot parse number of seats from {value!r}")
    return int(match.group())


def seats_forward(apps, schema_editor):
    ExchangeProgram = apps.get_model("exchange", "ExchangeProgram")
    for program in ExchangeProgram.objects.all():
        try:
            program.seats_count = parse_seats(program.seats)
        except ValueError as error:
            raise ValueError(f"{error} (program id={program.pk})") from error
        program.save(update_fields=["seats_count"])


def seats_backward(apps, schema_editor):
    # Lossy: only the number survives, so "2 місця" comes back as "2"
    # and "до 4" as "4".
    ExchangeProgram = apps.get_model("exchange", "ExchangeProgram")
    for program in ExchangeProgram.objects.all():
        program.seats = str(program.seats_count)
        program.save(update_fields=["seats"])


class Migration(migrations.Migration):

    dependencies = [
        ("exchange", "0005_exchangeprogram_seats_count"),
    ]

    operations = [
        migrations.RunPython(seats_forward, seats_backward),
    ]
