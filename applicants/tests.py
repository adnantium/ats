import json
from django.test import TestCase
from django.contrib.auth.models import User, Group
from django.urls import reverse
from rest_framework.test import (
    APITestCase,
    APIRequestFactory,
    force_authenticate,
    APIClient,
)
from applicants.views import ApplicantViewSet

class ATSAPITestCase(APITestCase):
    def create_test_user(
        self, username: str, email: str, password: str, group_names: list = []
    ):
        """Helper to create a testing user with the given username, email, password, and add groups."""
        user = User.objects.create_user(username, email, password)
        for group_name in group_names:
            user.groups.add(Group.objects.get(name=group_name))
        user.save()
        return user

class TestGetCreateApplicant(ATSAPITestCase):
    """Tests the ApplicantViewSet for GET and POST requests.
    Checks that users with the correct permissions can view and add applicants.
    Permissions tested: CanViewApplicants, CanAddApplicants
    """
    fixtures = ["groups.json"]
    url = reverse("applicant-list")
    client = APIClient()

    def setUp(self):
        self.username_can_view = "can_view_applicants"
        self.username_no_permissions = "no_permissions"
        self.username_can_view_add = "can_view_add_applicants"
        self.email = "email@email.com"
        self.password = "test-password"

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

    def test_get_applicant_list_unauthenticated(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    def test_get_applicant_list_can_view_applicants(self):
        self.client.login(username=self.username_can_view, password=self.password)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_get_applicant_list_no_permissions(self):
        self.client.login(username=self.username_no_permissions, password=self.password)
        
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

        response = self.client.post(self.url, {"name": "test applicant"})
        self.assertEqual(response.status_code, 403)

    def test_add_applicant_can_add_applicants(self):
        self.client.login(username=self.user_can_view_add_applicants, password=self.password)
        
        response = self.client.post(self.url, {"name": "test applicant"})
        self.assertEqual(response.status_code, 201)
        self.assertIn("uid", response.data)
        uid = response.data["uid"]
        
        url_detail = reverse("applicant-detail", kwargs={"pk": uid})
        response = self.client.get(url_detail)
        self.assertEqual(response.status_code, 200)

