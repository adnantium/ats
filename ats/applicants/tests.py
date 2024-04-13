"""Tests for the applicants app. Tests the ApplicantViewSet for GET, POST, and PATCH requests."""

from django.contrib.auth.models import User, Group
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient

from applicants.models import Applicant, APPROVED, REJECTED, PENDING


class ATSAPITestCase(APITestCase):
    """Helper base class for ATS API tests. Sets up test users and groups and
    utility methods."""

    fixtures = ["groups.json"]
    client = APIClient()

    email = "email@email.com"
    password = "test-password"

    def create_test_user(
        self, username: str, email: str, password: str, group_names: list = None
    ):
        """Helper to create a testing user with the given username, email, password,
        and add groups."""
        user = User.objects.create_user(username, email, password)
        for group_name in group_names:
            user.groups.add(Group.objects.get(name=group_name))
        user.save()
        return user


class TestGetCreateApplicant(ATSAPITestCase):
    """Tests the ApplicantViewSet for GET and POST requests.
    Checks that users with the correct permissions can view and add applicants.
    Permissions tested: CanViewApplicants, CanAddApplicants
    Urls: /applicants/ and /applicants/<uid>/
    """

    url = reverse("applicant-list")

    def setUp(self):
        self.username_can_view = "can_view_applicants"
        self.username_no_permissions = "no_permissions"
        self.username_can_view_add = "can_view_add_applicants"

        # can view applicants, not ADD
        self.user_can_view_applicants = self.create_test_user(
            username=self.username_can_view,
            email=self.email,
            password=self.password,
            group_names=["CanViewApplicants"],
        )

        # no permissions
        self.user_no_permissions = self.create_test_user(
            self.username_no_permissions, self.email, self.password
        )

        # can add and view applicants
        self.user_can_view_add_applicants = self.create_test_user(
            username=self.username_can_view_add,
            email=self.email,
            password=self.password,
            group_names=["CanAddApplicants", "CanViewApplicants"],
        )

        self.test_applicant = Applicant.objects.create(name="test applicant")

    def test_get_applicant_list_unauthenticated(self):
        """Check that unauthenticated users cannot view the applicant list."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    def test_get_applicant_list_no_permissions(self):
        """Checks that a user with no permissions cannot view the applicant list."""
        self.client.login(username=self.username_no_permissions, password=self.password)

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

        response = self.client.post(self.url, {"name": "test applicant"})
        self.assertEqual(response.status_code, 403)

    def test_get_applicant_list_can_view_applicants(self):
        """Checks that a user with the CanViewApplicants permission can view the applicant list."""
        self.client.login(username=self.username_can_view, password=self.password)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_add_applicant_can_add_applicants(self):
        """Checks that a user with the CanAddApplicants permission can add an applicant."""
        self.client.login(
            username=self.user_can_view_add_applicants, password=self.password
        )
        response = self.client.post(self.url, {"name": "test applicant"})
        self.assertEqual(response.status_code, 201)
        self.assertIn("uid", response.data)
        uid = response.data["uid"]

        updated_applicant = Applicant.objects.get(uid=uid)
        self.assertEqual(updated_applicant.status, PENDING)

        url_detail = reverse("applicant-detail", kwargs={"pk": uid})
        response = self.client.get(url_detail)
        self.assertEqual(response.status_code, 200)


class TestUpdateApplicant(ATSAPITestCase):
    """Tests the ApplicantViewSet for PATCH requests.
    Checks that users with the correct permissions can approve, reject, and
    update notes for applicants.
    Permissions tested: CanApproveApplicants, CanUpdateNote
    Urls: /applicants/<uid>/approve/, /applicants/<uid>/reject/, /applicants/<uid>/note/
    """

    def setUp(self):
        self.username_can_approve = "can_approve"
        self.username_no_permissions = "no_permissions"
        self.username_can_update_note = "can_update_note"

        # can approve applicants
        self.user_can_approve = self.create_test_user(
            username=self.username_can_approve,
            email=self.email,
            password=self.password,
            group_names=["CanApproveApplicants"],
        )

        # can update note only
        self.user_can_update_note = self.create_test_user(
            username=self.username_can_update_note,
            email=self.email,
            password=self.password,
            group_names=["CanUpdateNote"],
        )

        # no permissions at all
        self.user_no_permissions = self.create_test_user(
            self.username_no_permissions, self.email, self.password
        )

        self.test_applicant = Applicant.objects.create(name="test applicant")

    def test_update_applicant_unauthenticated(self):
        """Shouldnt be able to do anything if not authenticated so only 403s"""
        url = reverse("applicant-approve", kwargs={"pk": self.test_applicant.uid})
        response = self.client.patch(url)
        self.assertEqual(response.status_code, 403)

        url = reverse("applicant-reject", kwargs={"pk": self.test_applicant.uid})
        response = self.client.patch(url)
        self.assertEqual(response.status_code, 403)

        url = reverse("applicant-note", kwargs={"pk": self.test_applicant.uid})
        response = self.client.patch(url)
        self.assertEqual(response.status_code, 403)

    def test_update_applicant_no_permissions(self):
        """Checks authenticated user with no permissions cannot approve, reject, or 
        update notes."""
        self.client.login(username=self.username_no_permissions, password=self.password)

        url = reverse("applicant-approve", kwargs={"pk": self.test_applicant.uid})
        response = self.client.patch(url)
        self.assertEqual(response.status_code, 403)

        url = reverse("applicant-reject", kwargs={"pk": self.test_applicant.uid})
        response = self.client.patch(url)
        self.assertEqual(response.status_code, 403)

        url = reverse("applicant-note", kwargs={"pk": self.test_applicant.uid})
        response = self.client.patch(url)
        self.assertEqual(response.status_code, 403)

    def test_approve_reject_applicant_can_approve(self):
        """Checks that a user with the CanApproveApplicants permission can approve and 
        reject applicants."""
        self.client.login(username=self.username_can_approve, password=self.password)

        url = reverse("applicant-approve", kwargs={"pk": self.test_applicant.uid})
        response = self.client.patch(url)
        self.assertEqual(response.status_code, 202)
        updated_applicant = Applicant.objects.get(uid=self.test_applicant.uid)
        self.assertEqual(updated_applicant.status, APPROVED)

        url = reverse("applicant-reject", kwargs={"pk": self.test_applicant.uid})
        response = self.client.patch(url)
        self.assertEqual(response.status_code, 202)
        updated_applicant = Applicant.objects.get(uid=self.test_applicant.uid)
        self.assertEqual(updated_applicant.status, REJECTED)

    def test_update_note_applicant_can_update(self):
        """Checks that a user with the CanUpdateNote permission can update notes"""
        self.client.login(
            username=self.username_can_update_note, password=self.password
        )

        url = reverse("applicant-note", kwargs={"pk": self.test_applicant.uid})
        test_note = "updated note"
        response = self.client.patch(url, {"note": test_note})
        self.assertEqual(response.status_code, 202)
        updated_applicant = Applicant.objects.get(uid=self.test_applicant.uid)
        self.assertEqual(updated_applicant.note, test_note)
