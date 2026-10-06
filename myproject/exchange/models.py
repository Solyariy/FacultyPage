from django.db import models
from django.utils import timezone


class ExchangeProgram(models.Model):
    university = models.CharField("назва університету", max_length=200)
    country = models.CharField("країна", max_length=100, blank=True, default="")
    languages = models.CharField("мови навчання", max_length=200)
    seats = models.PositiveIntegerField("кількість місць")
    deadline = models.DateField("дедлайн подачі")
    description = models.TextField("опис")

    class Meta:
        ordering = ["deadline", "university"]
        verbose_name = "програма обміну"
        verbose_name_plural = "програми обміну"

    def __str__(self):
        return (
            f"{self.university} ({self.country})" if self.country else self.university
        )

    @property
    def is_open(self):
        return self.deadline >= timezone.localdate()
