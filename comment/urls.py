from django.urls import path

from .views import CommentView

urlpatterns = [
        path('/<int:song>', CommentView.as_view()),
        ]
