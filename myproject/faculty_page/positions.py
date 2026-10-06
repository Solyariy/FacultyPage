"""Personnel positions live in the database; this module mirrors them as a Python enum.

The enum is built on server start-up (see myproject/wsgi.py and asgi.py) and rebuilt
whenever a Position row is saved or deleted. Member name = Position.code, value = pk.
"""

import enum

from django.db import DatabaseError
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from faculty_page.models import Position

_labels = {}
PositionEnum = None


class PositionEnumBase(enum.Enum):
    @property
    def label(self):
        return _labels.get(self.value, self.name)


def load_position_enum():
    global PositionEnum
    try:
        rows = list(Position.objects.order_by("pk").values_list("pk", "code", "title"))
    except DatabaseError:
        # Tables don't exist yet (fresh DB, before migrate).
        return None
    _labels.clear()
    _labels.update({pk: title for pk, _, title in rows})
    PositionEnum = PositionEnumBase(
        "PositionEnum", [(code, pk) for pk, code, _ in rows]
    )
    return PositionEnum


def get_position_enum():
    return PositionEnum or load_position_enum()


@receiver([post_save, post_delete], sender=Position)
def reload_position_enum_on_change(**kwargs):
    load_position_enum()
