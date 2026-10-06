from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from faculty_page.models import (
    Department,
    Discipline,
    HomePage,
    Personnel,
    Position,
    Program,
)
from faculty_page.positions import get_position_enum


class FacultyPagesTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.docent = Position.objects.get(code="DOCENT")
        cls.dept = Department.objects.create(name="Кафедра історії")
        cls.other_dept = Department.objects.create(name="Кафедра культурології")
        cls.head = Personnel.objects.create(
            name="Іваненко Іван",
            position=cls.docent,
            degree="кандидат історичних наук",
            department=cls.dept,
        )
        cls.dept.head = cls.head
        cls.dept.save()
        cls.coordinator = Personnel.objects.create(
            name="Петренко Петро",
            position=cls.docent,
            contact="petro@ukma.edu.ua",
            department=cls.dept,
        )
        cls.discipline = Discipline.objects.create(
            name="Історія України", lecturer=cls.head
        )
        cls.program = Program.objects.create(
            name="Історія та археологія",
            code="032",
            description=" ".join(f"слово{i}" for i in range(80)),
            coordinator=cls.coordinator,
            department=cls.dept,
        )
        cls.program.disciplines.add(cls.discipline)

    def test_pages_ok(self):
        urls = [
            reverse("faculty:home"),
            reverse("faculty:program_list"),
            reverse("faculty:program_detail", args=[self.program.pk]),
            reverse("faculty:department_list"),
            reverse("faculty:department_detail", args=[self.dept.pk]),
        ]
        for url in urls:
            with self.subTest(url=url):
                self.assertEqual(self.client.get(url).status_code, 200)

    def test_missing_objects_404(self):
        self.assertEqual(
            self.client.get(reverse("faculty:program_detail", args=[999])).status_code,
            404,
        )
        self.assertEqual(
            self.client.get(
                reverse("faculty:department_detail", args=[999])
            ).status_code,
            404,
        )

    def test_program_list_truncates_description(self):
        response = self.client.get(reverse("faculty:program_list"))
        self.assertContains(response, "слово49")
        self.assertNotContains(response, "слово50")
        self.assertContains(response, self.program.get_absolute_url())
        self.assertContains(response, "Петренко Петро")
        self.assertContains(response, "petro@ukma.edu.ua")

    def test_program_detail_lists_disciplines(self):
        response = self.client.get(self.program.get_absolute_url())
        self.assertContains(response, "слово79")
        self.assertContains(response, "Історія України")
        self.assertContains(response, "Іваненко Іван")

    def test_department_pages(self):
        response = self.client.get(reverse("faculty:department_list"))
        self.assertContains(response, "Іваненко Іван")
        self.assertContains(response, self.program.get_absolute_url())

        response = self.client.get(self.dept.get_absolute_url())
        self.assertContains(response, "Петренко Петро")
        self.assertContains(response, "Доцент")
        self.assertContains(response, "кандидат історичних наук")
        self.assertContains(response, "032 Історія та археологія")

    def test_head_must_belong_to_department(self):
        self.other_dept.head = self.head
        with self.assertRaises(ValidationError):
            self.other_dept.full_clean()

    def test_home_page_load_on_empty_db(self):
        self.assertFalse(HomePage.objects.exists())
        self.assertEqual(HomePage.load().pk, 1)
        self.assertEqual(self.client.get(reverse("faculty:home")).status_code, 200)


class PositionEnumTest(TestCase):
    def test_enum_contains_db_positions(self):
        PositionEnum = get_position_enum()
        self.assertEqual(
            PositionEnum.PROFESSOR.value, Position.objects.get(code="PROFESSOR").pk
        )
        self.assertEqual(PositionEnum.PROFESSOR.label, "Професор")

    def test_enum_refreshes_on_change(self):
        get_position_enum()
        position = Position.objects.create(code="DEAN", title="Декан")
        self.assertEqual(get_position_enum().DEAN.value, position.pk)
        position.delete()
        self.assertFalse(hasattr(get_position_enum(), "DEAN"))
