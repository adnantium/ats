import uuid
from django.db import models


APPLICANT_STATUS_CHOICES = ["Pending", "Accepted", "Rejected"]


class Applicant(models.Model):
    uid = models.UUIDField(
        unique=True, primary_key=True, default=uuid.uuid4, editable=False
    )
    name = models.CharField(max_length=255)
    status = models.CharField(
        max_length=50,
        choices=[(c,c) for c in APPLICANT_STATUS_CHOICES],
        default=APPLICANT_STATUS_CHOICES[0],
    )
    note = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)


class HRManager(models.Model):
    uid = models.UUIDField(unique=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)


class HRManagerPermissions(models.Model):
    hr_manager = models.ForeignKey(HRManager, on_delete=models.CASCADE)
    view_applicant = models.BooleanField(default=False)
    create_applicant = models.BooleanField(default=False)
    accept_reject_applicant = models.BooleanField(default=False)
    update_notes = models.BooleanField(default=False)
