"""DRF's permission classes"""
from rest_framework.permissions import BasePermission


class CanAddApplicants(BasePermission):
    """User can add applicants. Note: This is separate from CanViewApplicants"""
    def has_permission(self, request, view) -> bool:
        return request.user.groups.filter(name="CanAddApplicants").exists()


class CanViewApplicants(BasePermission):
    """User can view existing applicants"""
    def has_permission(self, request, view) -> bool:
        return request.user.groups.filter(name="CanViewApplicants").exists()


class CanApproveApplicants(BasePermission):
    """Use can change the status of an applicant to 'Approved' or 'Rejected'"""
    def has_permission(self, request, view) -> bool:
        return request.user.groups.filter(name="CanApproveApplicants").exists()


class CanUpdateNote(BasePermission):
    """User can update the note field."""
    def has_permission(self, request, view) -> bool:
        return request.user.groups.filter(name="CanUpdateNote").exists()
