from django.contrib.auth.models import Group, User

can_add_applicants = Group.objects.get(name='CanAddApplicants')
can_view_applicants = Group.objects.get(name='CanViewApplicants')
can_approve_applicants = Group.objects.get(name='CanApproveApplicants')
can_update_note = Group.objects.get(name='CanUpdateNote')

user = User.objects.create(username='peter', password='django99', first_name='Peter', last_name='Parker')
user.groups.add(can_add_applicants)
user.groups.add(can_view_applicants)
user.groups.add(can_update_note)

user = User.objects.create(username='bruce', password='django99', first_name='Bruce', last_name='Wayne')
user.groups.add(can_view_applicants)
user.groups.add(can_approve_applicants)
