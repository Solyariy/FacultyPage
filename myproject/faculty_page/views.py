from django.shortcuts import get_object_or_404, render

from faculty_page.models import Department, HomePage, Personnel, Program


def home(request):
    return render(
        request,
        "faculty_page/home.html",
        {
            "page": HomePage.load(),
            "department_count": Department.objects.count(),
            "program_count": Program.objects.count(),
            "personnel_count": Personnel.objects.count(),
        },
    )


def program_list(request):
    programs = Program.objects.select_related("department", "coordinator")
    return render(request, "faculty_page/program_list.html", {"programs": programs})


def program_detail(request, pk):
    program = get_object_or_404(
        Program.objects.select_related("department", "coordinator"), pk=pk
    )
    return render(
        request,
        "faculty_page/program_detail.html",
        {
            "program": program,
            "disciplines": program.disciplines.select_related("lecturer"),
        },
    )


def department_list(request):
    departments = Department.objects.select_related("head__position").prefetch_related(
        "programs"
    )
    return render(
        request, "faculty_page/department_list.html", {"departments": departments}
    )


def department_detail(request, pk):
    department = get_object_or_404(
        Department.objects.select_related("head__position"), pk=pk
    )
    return render(
        request,
        "faculty_page/department_detail.html",
        {
            "department": department,
            "programs": department.programs.all(),
            "personnel": department.personnel.select_related("position"),
        },
    )
