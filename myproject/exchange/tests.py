import datetime
import importlib

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from exchange.models import ExchangeProgram

split_migration = importlib.import_module(
    "exchange.migrations.0004_split_university_country"
)
seats_migration = importlib.import_module("exchange.migrations.0006_convert_seats")


class SeededDataTest(TestCase):
    def test_seed_programs_are_migrated(self):
        self.assertEqual(ExchangeProgram.objects.count(), 6)
        expected = {
            "Uniwersytet Warszawski": ("Польща", 5),
            "KU Leuven": ("Бельгія", 2),
            "Vilnius University": ("Литва", 4),
            "Uniwersytet Jagielloński": ("Польща", 3),
            "University of Tartu": ("Естонія", 2),
            "Masaryk University": ("Чехія", 1),
        }
        actual = {
            program.university: (program.country, program.seats)
            for program in ExchangeProgram.objects.all()
        }
        self.assertEqual(actual, expected)

    def test_languages_kept_as_is(self):
        program = ExchangeProgram.objects.get(university="Uniwersytet Jagielloński")
        self.assertEqual(program.languages, "Польська, Англійська")


class MigrationHelpersTest(TestCase):
    def test_split_university(self):
        cases = {
            "Uniwersytet Warszawski, Польща": ("Uniwersytet Warszawski", "Польща"),
            "KU Leuven (Бельгія)": ("KU Leuven", "Бельгія"),
            "University of Tartu - Естонія": ("University of Tartu", "Естонія"),
            "Somewhere": ("Somewhere", ""),
        }
        for value, expected in cases.items():
            with self.subTest(value=value):
                self.assertEqual(split_migration.split_university(value), expected)

    def test_merge_university(self):
        self.assertEqual(
            split_migration.merge_university("KU Leuven", "Бельгія"),
            "KU Leuven, Бельгія",
        )
        self.assertEqual(split_migration.merge_university("Somewhere", ""), "Somewhere")

    def test_parse_seats(self):
        cases = {"5": 5, "2 місця": 2, "до 4": 4, "1 місце": 1}
        for value, expected in cases.items():
            with self.subTest(value=value):
                self.assertEqual(seats_migration.parse_seats(value), expected)
        with self.assertRaises(ValueError):
            seats_migration.parse_seats("уточнюється")


class ExchangePageTest(TestCase):
    def setUp(self):
        today = timezone.localdate()
        ExchangeProgram.objects.all().delete()
        self.open_program = ExchangeProgram.objects.create(
            university="Open University",
            country="Польща",
            languages="англійська",
            seats=2,
            deadline=today,
            description="Відкрита програма.",
        )
        self.closed_program = ExchangeProgram.objects.create(
            university="Closed University",
            country="Чехія",
            languages="англійська",
            seats=1,
            deadline=today - datetime.timedelta(days=1),
            description="Закрита програма.",
        )

    def test_is_open(self):
        self.assertTrue(self.open_program.is_open)
        self.assertFalse(self.closed_program.is_open)

    def test_page_shows_statuses(self):
        response = self.client.get(reverse("exchange:program_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Прийом триває")
        self.assertContains(response, "Прийом завершено")

    def test_country_filter(self):
        response = self.client.get(
            reverse("exchange:program_list"), {"country": "Польща"}
        )
        self.assertEqual(list(response.context["programs"]), [self.open_program])

    def test_header_link(self):
        response = self.client.get(reverse("faculty:home"))
        self.assertContains(response, reverse("exchange:program_list"))
