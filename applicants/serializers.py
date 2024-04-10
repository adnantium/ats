
from rest_framework import serializers
from applicants.models import Applicant, HRManager, HRManagerPermissions

class ApplicantSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Applicant
        fields = ['uid', 'name', 'status', 'note']
        read_only_fields = ('uid',)

class HRManagerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = HRManager
        fields = ['uid', 'name', 'email', 'password']
