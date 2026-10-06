from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse


class Position(models.Model):
    code = models.CharField("код", max_length=50, unique=True)
    title = models.CharField("назва", max_length=100)

    class Meta:
        ordering = ["title"]
        verbose_name = "посада"
        verbose_name_plural = "посади"

    def __str__(self):
        return self.title


class Personnel(models.Model):
    name = models.CharField("ім'я", max_length=200)
    position = models.ForeignKey(
        Position,
        on_delete=models.PROTECT,
        related_name="personnel",
        verbose_name="посада",
    )
    degree = models.CharField("науковий ступінь", max_length=200, blank=True)
    contact = models.CharField("контакт", max_length=200, blank=True)
    department = models.ForeignKey(
        "Department",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="personnel",
        verbose_name="кафедра",
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "працівник"
        verbose_name_plural = "працівники"

    def __str__(self):
        return self.name


class Department(models.Model):
    name = models.CharField("назва", max_length=200)
    head = models.ForeignKey(
        Personnel,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="headed_departments",
        verbose_name="завідувач кафедри",
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "кафедра"
        verbose_name_plural = "кафедри"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("faculty:department_detail", args=[self.pk])

    def clean(self):
        if self.head_id and self.pk and self.head.department_id != self.pk:
            raise ValidationError({"head": "Завідувач має працювати на цій кафедрі."})


class Discipline(models.Model):
    name = models.CharField("назва", max_length=200)
    description = models.TextField("опис", blank=True)
    lecturer = models.ForeignKey(
        Personnel,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="disciplines",
        verbose_name="викладач",
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "дисципліна"
        verbose_name_plural = "дисципліни"

    def __str__(self):
        return self.name


class Program(models.Model):
    name = models.CharField("назва", max_length=200)
    code = models.CharField("код", max_length=20)
    description = models.TextField("опис")
    coordinator = models.ForeignKey(
        Personnel,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="coordinated_programs",
        verbose_name="координатор набору",
    )
    department = models.ForeignKey(
        Department,
        on_delete=models.PROTECT,
        related_name="programs",
        verbose_name="випускова кафедра",
    )
    disciplines = models.ManyToManyField(
        Discipline, blank=True, related_name="programs", verbose_name="дисципліни"
    )

    class Meta:
        ordering = ["code", "name"]
        verbose_name = "спеціальність"
        verbose_name_plural = "спеціальності"

    def __str__(self):
        return f"{self.code} {self.name}"

    def get_absolute_url(self):
        return reverse("faculty:program_detail", args=[self.pk])


class HomePage(models.Model):
    title = models.CharField(
        "назва факультету", max_length=200, default="Факультет гуманітарних наук"
    )
    description = models.TextField("опис", blank=True)
    main_info = models.TextField("основна інформація", blank=True)
    address = models.CharField("адреса", max_length=300, blank=True)
    phone = models.CharField("телефон", max_length=50, blank=True)
    email = models.EmailField("email", blank=True)

    class Meta:
        verbose_name = "головна сторінка"
        verbose_name_plural = "головна сторінка"

    def __str__(self):
        return self.title

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj
