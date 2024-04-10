

from django.urls import path
from applicants.views import ApplicantListCreateAPIView, ApplicantDetail, CreateApplicant

app_name = 'applicants'

urlpatterns = [
    # path('', ApplicantListCreateAPIView.as_view()),
    path('', ApplicantListCreateAPIView.as_view()),
    # path('users', ListUsers.as_view()),
    path('<uuid:pk>/', ApplicantDetail.as_view(), name="detail"),
]
