from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Interest, InterestStatus
from .serializers import (
    InterestActionSerializer,
    InterestListSerializer,
    RejectInterestSerializer,
    SendInterestSerializer,
)
from .services.interest_service import accept_interest


class SendInterestView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = SendInterestSerializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        interest = serializer.save()
        output = InterestActionSerializer(interest)
        return Response(output.data, status=status.HTTP_201_CREATED)


class WithdrawInterestView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        try:
            interest = Interest.objects.select_related("sender").get(id=pk)
        except Interest.DoesNotExist:
            return Response(
                {"detail": "Interest not found."}, status=status.HTTP_404_NOT_FOUND
            )

        if interest.sender.user_id != request.user.id:
            return Response(
                {"detail": "You can withdraw only interests sent by you."},
                status=status.HTTP_403_FORBIDDEN,
            )

        if interest.status != InterestStatus.PENDING:
            return Response(
                {"detail": "Only pending interests can be withdrawn."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        interest.status = InterestStatus.WITHDRAWN
        interest.save(update_fields=["status", "last_action_at"])
        output = InterestActionSerializer(interest)
        return Response(output.data)


class AcceptInterestView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        try:
            interest = Interest.objects.select_related("receiver").get(id=pk)
        except Interest.DoesNotExist:
            return Response(
                {"detail": "Interest not found."}, status=status.HTTP_404_NOT_FOUND
            )

        if interest.receiver.user_id != request.user.id:
            return Response(
                {"detail": "You can accept only interests received by you."},
                status=status.HTTP_403_FORBIDDEN,
            )

        if interest.status != InterestStatus.PENDING:
            return Response(
                {"detail": "Only pending interests can be accepted."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        accept_interest(interest)
        interest.refresh_from_db()

        output = InterestActionSerializer(interest)
        return Response(output.data)


class RejectInterestView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        try:
            interest = Interest.objects.select_related("receiver").get(id=pk)
        except Interest.DoesNotExist:
            return Response(
                {"detail": "Interest not found."}, status=status.HTTP_404_NOT_FOUND
            )

        if interest.receiver.user_id != request.user.id:
            return Response(
                {"detail": "You can reject only interests received by you."},
                status=status.HTTP_403_FORBIDDEN,
            )

        if interest.status != InterestStatus.PENDING:
            return Response(
                {"detail": "Only pending interests can be rejected."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = RejectInterestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        interest.status = InterestStatus.REJECTED
        interest.rejection_reason_code = serializer.validated_data.get(
            "rejection_reason_code", ""
        )
        interest.save(
            update_fields=["status", "rejection_reason_code", "last_action_at"]
        )
        output = InterestActionSerializer(interest)
        return Response(output.data)


class ListReceivedInterestsView(generics.ListAPIView):
    serializer_class = InterestListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return (
            Interest.objects.select_related("sender", "receiver")
            .filter(receiver__user=self.request.user)
            .order_by("-created_at")
        )


class ListSentInterestsView(generics.ListAPIView):
    serializer_class = InterestListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return (
            Interest.objects.select_related("sender", "receiver")
            .filter(sender__user=self.request.user)
            .order_by("-created_at")
        )
