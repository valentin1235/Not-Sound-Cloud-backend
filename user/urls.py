from django.urls import path

from .views import (
        WebSignUpView,
        AppSignUpView,
        SignInView,
        MessageView,
        FollowView,
        UserRecommendationView,
        GoogleSignInView,
        NotificationView,
        StatusView,
        UserInfoView,
        UserSearchView,
        )

urlpatterns = [
        path('/sign-up', WebSignUpView.as_view()),
        path('/sign-in', SignInView.as_view()),
        path('/message', MessageView.as_view()),
        path('/follow', FollowView.as_view()),
        path('/sign-up/app', AppSignUpView.as_view()),
        path('/recommendation', UserRecommendationView.as_view()),
        path('/sign-up/google', GoogleSignInView.as_view()),
        path('/notification', NotificationView.as_view()),
        path('/status', StatusView.as_view()),
        path('', UserInfoView.as_view()),
        path('/search', UserSearchView.as_view()),
        ]

