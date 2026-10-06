from django.contrib import admin

from faculty_page.models import (
    Department,
    Discipline,
    HomePage,
    Personnel,
    Position,
    Program,
)


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ("title", "code")
    search_fields = ("title", "code")


@admin.register(Personnel)
class PersonnelAdmin(admin.ModelAdmin):
    list_display = ("name", "position", "degree", "department")
    list_filter = ("department", "position")
    search_fields = ("name",)


class PersonnelInline(admin.TabularInline):
    model = Personnel
    extra = 0
    fields = ("name", "position", "degree", "contact")


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("name", "head")
    search_fields = ("name",)
    autocomplete_fields = ("head",)
    inlines = [PersonnelInline]


@admin.register(Discipline)
class DisciplineAdmin(admin.ModelAdmin):
    list_display = ("name", "lecturer")
    search_fields = ("name",)
    autocomplete_fields = ("lecturer",)


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "department", "coordinator")
    list_filter = ("department",)
    search_fields = ("name", "code")
    autocomplete_fields = ("coordinator",)
    filter_horizontal = ("disciplines",)


@admin.register(HomePage)
class HomePageAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return not HomePage.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False
