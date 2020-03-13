from django.urls import path

from .views import SignUpView, SignInView, MessageView, FollowView

urlpatterns = [
        path('/sign-up', SignUpView.as_view()),
        path('/sign-in', SignInView.as_view()),
        path('/message', MessageView.as_view()),
        path('/follow', FollowView.as_view()),
        ]

