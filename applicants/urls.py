

from django.urls import path
from applicants.views import ApplicantListCreateAPIView

app_name = 'applicants'

urlpatterns = [
    path('applicants/', ApplicantListCreateAPIView.as_view()),
    # path('<int:pk>/', TodoDetailAPIView.as_view(), name="detail"),
]
