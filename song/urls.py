from django.urls import path
from .views import SongView,playView,SongUploadView,Test
from django.conf.urls.static import static
from  django.contrib.staticfiles.urls import  staticfiles_urlpatterns
from django.conf import settings
urlpatterns = [
    path('/<slug:option>/<int:song_id>',SongView.as_view()),
    path('/playview/<int:song_id>/<int:seconds>',playView.as_view()),
    path('/upload',SongUploadView.as_view()),
    path('/test',Test.as_view()),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL,document_root=settings)

