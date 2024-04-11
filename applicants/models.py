import uuid
from django.db import models

PENDING = "Pending"
APPROVED = "Approved"
REJECTED = "Rejected"
APPLICANT_STATUS_CHOICES = [PENDING, APPROVED, REJECTED]


class Applicant(models.Model):
    uid = models.UUIDField(
        unique=True, primary_key=True, default=uuid.uuid4, editable=False
    )
    name = models.CharField(max_length=255)
    status = models.CharField(
        max_length=50,
        choices=[(c, c) for c in APPLICANT_STATUS_CHOICES],
        default=PENDING,
    )
    note = models.TextField(blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def approve_applicant(self) -> None:
        self.status = APPROVED
        self.save()

    def reject_applicant(self) -> None:
        self.status = REJECTED
        self.save()

    def update_note(self, text) -> None:
        self.note = text
        self.save()
