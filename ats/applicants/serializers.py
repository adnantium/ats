"""serializers.py - For converting Django models to/from JSON"""
from rest_framework import serializers
from applicants.models import Applicant

class ApplicantSerializer(serializers.HyperlinkedModelSerializer):
    """Converts the Django model for Applicant to JSON and vice versa."""
    class Meta:
        model = Applicant
        fields = ["uid", "name", "status", "note"]
        read_only_fields = ("uid",)
