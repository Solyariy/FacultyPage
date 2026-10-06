from django.db import migrations

DEFAULT_POSITIONS = [
    ("PROFESSOR", "Професор"),
    ("DOCENT", "Доцент"),
    ("SENIOR_LECTURER", "Старший викладач"),
    ("LECTURER", "Викладач"),
    ("ASSISTANT", "Асистент"),
    ("LAB_HEAD", "Завідувач лабораторії"),
]


def add_positions(apps, schema_editor):
    Position = apps.get_model("faculty_page", "Position")
    for code, title in DEFAULT_POSITIONS:
        Position.objects.get_or_create(code=code, defaults={"title": title})


def remove_positions(apps, schema_editor):
    Position = apps.get_model("faculty_page", "Position")
    Position.objects.filter(code__in=[code for code, _ in DEFAULT_POSITIONS]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("faculty_page", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(add_positions, remove_positions),
    ]
