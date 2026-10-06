from django.contrib import admin

from exchange.models import ExchangeProgram


@admin.register(ExchangeProgram)
class ExchangeProgramAdmin(admin.ModelAdmin):
    list_display = (
        "university",
        "country",
        "languages",
        "seats",
        "deadline",
        "admission_open",
    )
    list_filter = ("country",)
    search_fields = ("university", "country")

    @admin.display(boolean=True, description="прийом триває")
    def admission_open(self, obj):
        return obj.is_open
