from django.conf.urls import url
from .views import AynalizeView, CodeDetailView

urlpatterns = [
    url(r'create/', AynalizeView.as_view()),
    url(r'detail/', CodeDetailView.as_view())
]
