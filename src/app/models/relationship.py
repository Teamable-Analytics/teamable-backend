from django.db import models

from app.models.base_models import BaseModel
from app.models.course_member import CourseMember


class RelationshipType(models.TextChoices):
    FRIEND = "Friend", "Friend"
    ENEMY = "Enemy", "Enemy"


class Relationship(BaseModel):
    """
    Models an "IS-A" relationship between two enrolled users.

    i.e. [from_member] is a [relationship] with [to_member]
    """

    from_member = models.ForeignKey(
        CourseMember, on_delete=models.CASCADE, related_name="outbound_relationships"
    )
    to_member = models.ForeignKey(
        CourseMember, on_delete=models.CASCADE, related_name="inbound_relationships"
    )
    type = models.CharField(max_length=10, choices=RelationshipType.choices)

    class Meta:
        unique_together = ["from_member", "to_member"]
