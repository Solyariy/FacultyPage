from django.apps import AppConfig


class FacultyPageConfig(AppConfig):
    name = "faculty_page"
    verbose_name = "Факультет"

    def ready(self):
        # Registers the Position signal receivers; no DB access here.
        from faculty_page import positions  # noqa: F401
