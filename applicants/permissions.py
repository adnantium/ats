from rest_framework.permissions import BasePermission


class CanAddApplicants(BasePermission):
    def has_permission(self, request, view) -> bool:
        return request.user.groups.filter(name="CanAddApplicants").exists()


class CanViewApplicants(BasePermission):
    def has_permission(self, request, view) -> bool:
        return request.user.groups.filter(name="CanViewApplicants").exists()


class CanApproveApplicants(BasePermission):
    def has_permission(self, request, view) -> bool:
        return request.user.groups.filter(name="CanApproveApplicants").exists()


class CanUpdateNote(BasePermission):
    def has_permission(self, request, view) -> bool:
        return request.user.groups.filter(name="CanUpdateNote").exists()
