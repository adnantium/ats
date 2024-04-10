
from rest_framework import permissions, viewsets
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from .models import Applicant, HRManager, HRManagerPermissions
from .serializers import ApplicantSerializer, HRManagerSerializer
from .permissions import CanViewApplicants


class ApplicantViewSet(viewsets.ModelViewSet):
    queryset = Applicant.objects.all().order_by('name')
    serializer_class = ApplicantSerializer
    permission_classes = [CanViewApplicants]


class HRManagerViewSet(viewsets.ModelViewSet):
    queryset = HRManager.objects.all().order_by('name')
    serializer_class = HRManagerSerializer
    # permission_classes = [permissions.IsAuthenticated]


class ApplicantListCreateAPIView(ListCreateAPIView):
    serializer_class = ApplicantSerializer
    def get_queryset(self):
        return Applicant.objects.all().order_by('name')
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
