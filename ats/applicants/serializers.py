from rest_framework import serializers
from applicants.models import Applicant


class ApplicantSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Applicant
        fields = ["uid", "name", "status", "note"]
        read_only_fields = ("uid",)
