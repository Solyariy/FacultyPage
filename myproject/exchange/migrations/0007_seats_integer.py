from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("exchange", "0006_convert_seats"),
    ]

    # Reversed, RemoveField re-creates the text "seats" column. The temporary
    # default="" lets it be added NOT NULL to a table that already has rows;
    # 0006's backward step then writes the numbers into it.
    operations = [
        migrations.AlterField(
            model_name="exchangeprogram",
            name="seats",
            field=models.CharField(
                default="", max_length=50, verbose_name="кількість місць"
            ),
        ),
        migrations.RemoveField(
            model_name="exchangeprogram",
            name="seats",
        ),
        migrations.RenameField(
            model_name="exchangeprogram",
            old_name="seats_count",
            new_name="seats",
        ),
        migrations.AlterField(
            model_name="exchangeprogram",
            name="seats",
            field=models.PositiveIntegerField(verbose_name="кількість місць"),
        ),
    ]
