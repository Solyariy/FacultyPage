"""Fill the DB with Faculty of Humanities (NaUKMA) data taken from the public faculty page.

Only facts present on the source page are seeded; unknown fields stay blank.
Disciplines are sample entries to demonstrate the program page. Safe to run repeatedly.
"""

from django.core.management.base import BaseCommand
from django.db import transaction

from faculty_page.models import (
    Department,
    Discipline,
    HomePage,
    Personnel,
    Position,
    Program,
)

DEPARTMENTS = [
    "Кафедра англійської мови",
    "Кафедра археології",
    "Кафедра історії",
    "Кафедра філософії та релігієзнавства",
    "Кафедра культурології",
    "Кафедра літературознавства ім. В. Моренця",
    "Кафедра загального та слов'янського мовознавства",
    "Кафедра української мови",
]

# name, position code, degree, department (or None)
PERSONNEL = [
    ("Мазін Дмитро Михайлович", "DOCENT", "кандидат філологічних наук", None),
    (
        "Юринець Ярина Ігорівна",
        "SENIOR_LECTURER",
        "",
        "Кафедра філософії та релігієзнавства",
    ),
    (
        "Менжулін Вадим",
        "HEAD_OF_DEPARTMENT",
        "",
        "Кафедра філософії та релігієзнавства",
    ),
    (
        "Куранова Світлана",
        "HEAD_OF_DEPARTMENT",
        "",
        "Кафедра загального та слов'янського мовознавства",
    ),
]

HEADS = {
    "Кафедра філософії та релігієзнавства": "Менжулін Вадим",
    "Кафедра загального та слов'янського мовознавства": "Куранова Світлана",
}

# code, name, department, description, sample disciplines
PROGRAMS = [
    (
        "032",
        "Історія та археологія",
        "Кафедра історії",
        "Бакалаврська програма з історії та археології: від джерелознавства й археологічних "
        "практик до сучасних підходів у дослідженні минулого України, Європи та світу.",
        ["Історія України", "Вступ до археології", "Джерелознавство"],
    ),
    (
        "033",
        "Філософія",
        "Кафедра філософії та релігієзнавства",
        "Бакалаврська програма з філософії: історія філософської думки, логіка, етика, "
        "філософія свідомості та релігієзнавство.",
        ["Вступ до філософії", "Логіка", "Етика"],
    ),
    (
        "034",
        "Культурологія",
        "Кафедра культурології",
        "Бакалаврська програма з культурології: теорія та історія культури, візуальні студії, "
        "кіностудії й аналіз сучасних культурних практик.",
        ["Теорія культури", "Історія світової культури"],
    ),
    (
        "035.01",
        "Українська мова та література",
        "Кафедра української мови",
        "Бакалаврська програма з філології (українська мова та література): мовознавство, "
        "літературознавство, редагування та викладання.",
        ["Сучасна українська літературна мова", "Теорія літератури"],
    ),
    (
        "035.041",
        "Англійська та українська мови",
        "Кафедра англійської мови",
        "Бакалаврська програма з філології (германські мови та літератури): англійська та "
        "українська мови, переклад, мовна комунікація.",
        ["Практичний курс англійської мови", "Вступ до мовознавства"],
    ),
]


class Command(BaseCommand):
    help = "Заповнює БД даними факультету гуманітарних наук НаУКМА."

    @transaction.atomic
    def handle(self, *args, **options):
        page = HomePage.load()
        page.title = "Факультет гуманітарних наук"
        page.description = (
            "Факультет гуманітарних наук НаУКМА — науково-освітній підрозділ, створений "
            "під час відродження Києво-Могилянської академії. Об’єднує вісім кафедр і "
            "поєднує викладання, дослідження, просвітницьку та культурну діяльність."
        )
        page.main_info = (
            "Декан: Мазін Дмитро Михайлович, кандидат філологічних наук, доцент.\n"
            "Заступниця декана: Юринець Ярина Ігорівна.\n"
            "Бакалаврат, магістратура та PhD з історії, археології, філософії, "
            "культурології та філології."
        )
        page.address = "м. Київ, вул. Григорія Сковороди, 2, корпус 1, кімната 201"
        page.phone = "(044) 425-14-20"
        page.save()

        Position.objects.get_or_create(
            code="HEAD_OF_DEPARTMENT", defaults={"title": "Завідувач кафедри"}
        )
        positions = {p.code: p for p in Position.objects.all()}

        departments = {
            name: Department.objects.get_or_create(name=name)[0] for name in DEPARTMENTS
        }

        people = {}
        for name, position, degree, department in PERSONNEL:
            people[name], _ = Personnel.objects.update_or_create(
                name=name,
                defaults={
                    "position": positions[position],
                    "degree": degree,
                    "department": departments.get(department),
                },
            )

        for department, head in HEADS.items():
            departments[department].head = people[head]
            departments[department].save()

        for code, name, department, description, discipline_names in PROGRAMS:
            program, _ = Program.objects.update_or_create(
                code=code,
                name=name,
                defaults={
                    "department": departments[department],
                    "description": description,
                },
            )
            program.disciplines.set(
                Discipline.objects.get_or_create(name=d)[0] for d in discipline_names
            )

        self.stdout.write(
            self.style.SUCCESS(
                f"Готово: {Department.objects.count()} кафедр, {Program.objects.count()} спеціальностей, "
                f"{Personnel.objects.count()} працівників, {Discipline.objects.count()} дисциплін."
            )
        )
