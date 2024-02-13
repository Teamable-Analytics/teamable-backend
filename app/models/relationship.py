from django.db import models
from django.utils.translation import gettext_lazy as _

from app.models.base_models import TimeStampedModel
from app.models.enrollment import Enrollment


class RelationshipType(models.TextChoices):
    FRIEND = "F", _("friend")
    ENEMY = "E", _("enemy")


class Relationship(TimeStampedModel):
    """
    Models an "IS-A" relationship between two enrolled users.

    i.e. [from_user] is a [relationship] with [to_user]
    """

    from_user = models.ForeignKey(
        Enrollment, on_delete=models.CASCADE, related_name="relationships"
    )
    to_user = models.ForeignKey(Enrollment, on_delete=models.CASCADE)
    type = models.CharField(max_length=1, choices=RelationshipType.choices)

    class Meta:
        unique_together = ["from_user", "to_user"]
