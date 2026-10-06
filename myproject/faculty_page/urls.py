from django.urls import path

from faculty_page import views

app_name = "faculty"

urlpatterns = [
    path("", views.home, name="home"),
    path("programs/", views.program_list, name="program_list"),
    path("programs/<int:pk>/", views.program_detail, name="program_detail"),
    path("departments/", views.department_list, name="department_list"),
    path("departments/<int:pk>/", views.department_detail, name="department_detail"),
]
