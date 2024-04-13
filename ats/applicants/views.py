"""docstring for views.py"""
import uuid
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.exceptions import PermissionDenied

from django.shortcuts import get_object_or_404

from .models import Applicant
from .serializers import ApplicantSerializer
from .permissions import (
    CanViewApplicants,
    CanApproveApplicants,
    CanAddApplicants,
    CanUpdateNote,
)

class ApplicantViewSet(ModelViewSet):
    """Contains all views for the Applicant model GET/POST/PATCH endpoints."""
    
    queryset = Applicant.objects.all().order_by("name")
    serializer_class = ApplicantSerializer
    permission_classes = [CanViewApplicants]

    def create(self, request: Request) -> Response:
        """Extension of default create() method that also checks for 
        CanAddApplicants permissions."""
        if not CanAddApplicants().has_permission(request=request, view=self):
            raise PermissionDenied()
        return super().create(request)

    @action(
        methods=["PATCH"],
        detail=True,
        permission_classes=[CanApproveApplicants],
        url_path="approve",
        url_name="approve",
    )
    def approve(self, request: Request, pk: uuid.UUID) -> Response:
        """Updates the status of an applicant to 'Approved'."""
        applicant = get_object_or_404(Applicant, pk=pk)
        applicant.approve_applicant()
        return Response(
            ApplicantSerializer(applicant).data, status=status.HTTP_202_ACCEPTED
        )

    @action(
        methods=["PATCH"],
        detail=True,
        permission_classes=[CanApproveApplicants],
        url_path="reject",
        url_name="reject",
    )
    def reject(self, request: Request, pk: uuid.UUID) -> Response:
        """Updates the status of an applicant to 'Rejected'."""
        applicant = get_object_or_404(Applicant, pk=pk)
        applicant.reject_applicant()
        return Response(
            ApplicantSerializer(applicant).data, status=status.HTTP_202_ACCEPTED
        )

    @action(
        methods=["PATCH"],
        detail=True,
        permission_classes=[CanUpdateNote],
        url_path="note",
        url_name="note",
    )
    def update_note(self, request: Request, pk: uuid.UUID) -> Response:
        """Updates the note of an applicant."""
        applicant = get_object_or_404(Applicant, pk=pk)
        if text := request.data.get("note"):
            applicant.update_note(text)
            return Response(
                ApplicantSerializer(applicant).data, status=status.HTTP_202_ACCEPTED
            )
        return Response(
            {"status": "fail", "message": "note is required"},
            status=status.HTTP_400_BAD_REQUEST,
        )
