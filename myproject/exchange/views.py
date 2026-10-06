from django.shortcuts import render

from exchange.models import ExchangeProgram


def program_list(request):
    programs = ExchangeProgram.objects.all()
    countries = (
        ExchangeProgram.objects.exclude(country="")
        .order_by("country")
        .values_list("country", flat=True)
        .distinct()
    )
    country = request.GET.get("country", "")
    if country:
        programs = programs.filter(country=country)
    return render(
        request,
        "exchange/program_list.html",
        {"programs": programs, "countries": countries, "country": country},
    )
