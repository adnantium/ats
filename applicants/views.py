from rest_framework import permissions, viewsets
from rest_framework.generics import ListCreateAPIView
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied

from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from .models import Applicant
from .serializers import ApplicantSerializer
from .permissions import (
    CanViewApplicants,
    CanApproveApplicants,
    CanAddApplicants,
    CanUpdateNote,
)


class ApplicantViewSet(viewsets.ModelViewSet):
    queryset = Applicant.objects.all().order_by("name")
    serializer_class = ApplicantSerializer
    permission_classes = [CanViewApplicants]

    def create(self, request, *args, **kwargs):
        if not CanAddApplicants().has_permission(request=request, view=self):
            raise PermissionDenied()
        return super().create(request, *args, **kwargs) 

    @action(
        methods=["PATCH"],
        detail=True,
        permission_classes=[CanApproveApplicants],
        url_path="approve",
        url_name="approve",
    )
    def approve(self, request, pk=None):
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
    def reject(self, request, pk=None):
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
    def update_note(self, request, pk=None):
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



# class ApplicantListCreateAPIView(ListCreateAPIView):
#     serializer_class = ApplicantSerializer
#     permission_classes = (CanViewApplicants,)

#     def get_queryset(self):
#         return Applicant.objects.all().order_by("name")

#     def perform_create(self, serializer):
#         if "applicants.add_applicant" not in self.request.user.get_group_permissions():
#             raise PermissionDenied()
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(
#             {"status": "fail", "message": serializer.errors},
#             status=status.HTTP_400_BAD_REQUEST,
#         )


# class ApplicantDetail(APIView):
#     permission_classes = (CanViewApplicants,)

#     def get(self, request, pk, format=None):
#         applicant = get_object_or_404(Applicant, pk=pk)
#         serializer = ApplicantSerializer(applicant)
#         # self.check_object_permissions(request, applicant)
#         return Response(serializer.data)


# class CreateApplicant(APIView):
#     permission_classes = (CanAddApplicants,)

#     def post(self, request, format=None):
#         serializer = ApplicantSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['POST'])
# def create_applicant(request):
#     serializer = ApplicantSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['PATCH'])
# def approve_reject_applicant(request):
#     pass
#     # serializer = ApplicantSerializer(data=request.data)
#     # if serializer.is_valid():
#     #     serializer.save()
#     #     return Response(serializer.data, status=status.HTTP_201_CREATED)
#     # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
