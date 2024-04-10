from rest_framework.permissions import BasePermission
from django.contrib.auth.models import User, Group

class CanAddApplicants(BasePermission):
    def has_permission(self, request, view):
        # todo: use proper django query to check this
        return Group.objects.get(name='CanAddApplicants') in request.user.groups.all()
    
class CanViewApplicants(BasePermission):
    def has_permission(self, request, view):
        # todo: use proper django query to check this
        return Group.objects.get(name='CanViewApplicants') in request.user.groups.all()
    
class CanApproveApplicants(BasePermission):
    def has_permission(self, request, view):
        # todo: use proper django query to check this
        return Group.objects.get(name='CanApproveApplicants') in request.user.groups.all()
    
class CanUpdateNote(BasePermission):
    def has_permission(self, request, view):
        # todo: use proper django query to check this
        return Group.objects.get(name='CanUpdateNote') in request.user.groups.all()



# view_applicant
# create_applicant
# accept_reject_applicant
# update_notes
