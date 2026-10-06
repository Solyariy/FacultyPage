from django import template

register = template.Library()


@register.filter
def initials(name):
    """'Мазін Дмитро Михайлович' -> 'МД'."""
    parts = str(name).split()
    return "".join(part[0] for part in parts[:2]).upper()


@register.filter
def uk_plural(count, forms):
    """Pick the Ukrainian plural form: {{ n|uk_plural:"кафедра,кафедри,кафедр" }}."""
    one, few, many = forms.split(",")
    count = abs(int(count))
    if count % 10 == 1 and count % 100 != 11:
        return one
    if 2 <= count % 10 <= 4 and not 12 <= count % 100 <= 14:
        return few
    return many
