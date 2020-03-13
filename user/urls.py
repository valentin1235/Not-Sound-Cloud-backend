from django.urls import path

from .views import (
        WebSignUpView,
        AppSignUpView,
        SignInView,
        MessageView,
        FollowView,
        UserRecommendationView,
        )

urlpatterns = [
        path('/sign-up', WebSignUpView.as_view()),
        path('/sign-in', SignInView.as_view()),
        path('/message', MessageView.as_view()),
        path('/follow', FollowView.as_view()),
        path('/sign-up/app', AppSignUpView.as_view()),
        path('/recommendation', UserRecommendationView.as_view()),
        ]

