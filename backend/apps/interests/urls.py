from django.urls import path
from .views import (
    AcceptInterestView,
    ListReceivedInterestsView,
    ListSentInterestsView,
    RejectInterestView,
    SendInterestView,
    WithdrawInterestView,
)

urlpatterns = [
    path("send/", SendInterestView.as_view()),
    path("<uuid:pk>/withdraw/", WithdrawInterestView.as_view()),
    path("<uuid:pk>/accept/", AcceptInterestView.as_view()),
    path("<uuid:pk>/reject/", RejectInterestView.as_view()),
    path("received/", ListReceivedInterestsView.as_view()),
    path("sent/", ListSentInterestsView.as_view()),
]
