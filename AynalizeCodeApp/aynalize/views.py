from django.conf import settings
from .base import CreateBaseAPIView, GetDetailAPIView
from .base import API_KIND_DETAIL
from .utils import *
from logging import getLogger

logger = getLogger('django')


# Create your views here.

class AynalizeView(CreateBaseAPIView):
    """
    Aynalize code class
    """

    def __init__(self):
        super(AynalizeView, self).__init__()

    def do_aynalize(self):
        """
        override method to do aynalize code
        :return:
        """
        result = True
        # todo involve aynalize helper method in utils

        return result


class CodeDetailView(GetDetailAPIView):
    """
    Get the code detail information class
    """

    def __init__(self):
        super(CodeDetailView, self).__init__()

    def get_queryset(self):
        """
        This function is override base get_queryset
        :return: queryset
        """

        query_set = None
        return query_set

    def get_serializer_class(self):
        """
        Override the get_serializer_class() method
        :return:
        """

        if self.api_kind == API_KIND_DETAIL:
            return None
        return None

