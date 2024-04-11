import json
from django.test import TestCase
from django.contrib.auth.models import User, Group
from django.urls import reverse
from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate, APIClient
from applicants.views import ApplicantViewSet

class TestGetApplicantList(APITestCase):
    fixtures = ['groups.json']
    url = reverse("applicant-list")
    client = APIClient()
    
    def setUp(self):
        self.username_can_view = "can_view_applicants"
        self.username_cannot_view = "cannot_view_applicants"
        self.email = "john@snow.com"
        self.password = "test-password"

        self.user_can_view_applicants = User.objects.create_user(self.username_can_view, self.email, self.password)
        self.user_can_view_applicants.groups.add(Group.objects.get(name='CanViewApplicants'))
        self.user_can_view_applicants.save()

        self.user_cannot_view_applicants = User.objects.create_user(self.username_cannot_view, self.email, self.password)

    def test_get_applicant_list_unauthenticated(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    def test_get_applicant_list_can_view_applicants(self):
        self.client.login(username=self.username_can_view, password=self.password)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        
    def test_get_applicant_list_cannot_view_applicants(self):
        self.client.login(username=self.username_cannot_view, password=self.password)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)
        

    # def test_user_(self):
    #     Applicant.objects.create(user=self.user, name="Clean the car!")
    #     response = self.client.get(self.url)
    #     self.assertTrue(len(json.loads(response.content)) == Applicant.objects.count())




# class UserLoginAPIViewTestCase(APITestCase):
#     url = reverse("users:login")

#     def setUp(self):
#         self.username = "john"
#         self.email = "john@snow.com"
#         self.password = "you_know_nothing"
#         self.user = User.objects.create_user(self.username, self.email, self.password)

#     def test_authentication_without_password(self):
#         response = self.client.post(self.url, {"username": "snowman"})
#         self.assertEqual(400, response.status_code)

#     def test_authentication_with_wrong_password(self):
#         response = self.client.post(self.url, {"username": self.username, "password": "I_know"})
#         self.assertEqual(400, response.status_code)

#     def test_authentication_with_valid_data(self):
#         response = self.client.post(self.url, {"username": self.username, "password": self.password})
#         self.assertEqual(200, response.status_code)
#         self.assertTrue("auth_token" in json.loads(response.content))
