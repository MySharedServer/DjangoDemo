from django.conf.urls import url
from .views import AynalizeView, CodeDetailView, CodeSearchView

urlpatterns = [
    url(r'create/', AynalizeView.as_view()),
    url(r'detail/', CodeDetailView.as_view()),
    url(r'search/', CodeSearchView.as_view()),
]
