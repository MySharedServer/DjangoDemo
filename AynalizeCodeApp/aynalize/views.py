from django.conf import settings
from django import db
from django.db.utils import IntegrityError
from django.db.models import Count
from .base import CreateBaseAPIView, GetDetailAPIView
from .base import API_KIND_DETAIL
from .models import FunctionInfo
from .utils import *
from logging import getLogger

logger = getLogger('django')

KEY_FILE_NAME = 'fileName'
KEY_FUNC_DETAIL = 'funcDetail'
KEY_FUNC_DETAIL_NAME = 'name'
KEY_FUNC_DETAIL_PARAM = 'params'
KEY_FUNC_DETAIL_BODY = 'body'
KEY_FUNC_DETAIL_LINE = 'line'

FIELD_FILE_NAME = 'fileName'
FIELD_FUNC_NAME = 'name'
FIELD_FUNC_PARAM = 'params'
FIELD_FUNC_BODY = 'body'
FIELD_FUNC_LINE = 'line'


# Create your views here.

class AynalizeView(CreateBaseAPIView):
    """
    Aynalize code class
    """

    create_objects_count = 0

    def __init__(self):
        super(AynalizeView, self).__init__()

    def do_aynalize(self):
        """
        override method to do aynalize code
        :return:
        """
        result = True
        # todo involve aynalize helper method in utils
        file_list = [
            {
                'fileName': 'test file name1',
                'funcDetail': [
                    {
                        'name': 'test function1_1',
                        'params': 'none',
                        'body': 'test body',
                        'line': '2',
                        'fileName': 'test file name1'
                    },
                    {
                        'name': 'test function1_2',
                        'params': 'none',
                        'body': 'test body',
                        'line': '12',
                        'fileName': 'test file name1'
                    },

                ]
            },
            {
                'fileName': 'test file name2',
                'funcDetail': [
                    {
                        'name': 'test function2_1',
                        'params': 'none',
                        'body': 'test body',
                        'line': '20',
                        'fileName': 'test file name2'
                    },
                    {
                        'name': 'test function2_2',
                        'params': 'none',
                        'body': 'test body',
                        'line': '30',
                        'fileName': 'test file name2'
                    },

                ]
            },

        ]
        result = self.bulk_insert(file_list)

        return result

    def bulk_insert(self, file_list, delete=True):
        """
        List data bulk_create
        :param file_list: list type
        :param delete: delete record
        :return: result
        """

        result = True
        m = len(file_list)
        cnt = 0
        if m > 0:
            data_array = []
            for data in file_list:
                cnt += len(data.get(KEY_FUNC_DETAIL, []))
                for obj in data.get(KEY_FUNC_DETAIL, []):

                    data_array.append(
                        FunctionInfo(
                            fileName=obj[KEY_FILE_NAME],
                            name=obj[KEY_FUNC_DETAIL_NAME],
                            params=obj[KEY_FUNC_DETAIL_PARAM],
                            body=obj[KEY_FUNC_DETAIL_BODY],
                            line=obj[KEY_FUNC_DETAIL_LINE],
                        )
                    )

            try:
                if delete:
                    FunctionInfo.objects.all().delete()
                FunctionInfo.objects.bulk_create(data_array)
            except IntegrityError:
                result = False
                logger.info("{0}: database bulk create error".format(self.__class__.__name__))
            else:
                self.create_objects_count = cnt
            # Django Query reset
            db.reset_queries()

        logger.info("{0}: create function record count: {1}".format(self.__class__.__name__, self.create_objects_count))
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

        data_list = []
        file_list = FunctionInfo.objects.values(FIELD_FILE_NAME).annotate(fileCnt=Count(FIELD_FILE_NAME))
        for file in file_list:
            logger.info("{0}: file name:{1}".format(self.__class__.__name__, file.get(FIELD_FILE_NAME)))
            file_dict = {}
            file_dict[KEY_FILE_NAME] = file.get(FIELD_FILE_NAME)

            query_set = FunctionInfo.objects.filter(fileName=file.get(FIELD_FILE_NAME)).values(
                FIELD_FILE_NAME, FIELD_FUNC_NAME, FIELD_FUNC_PARAM, FIELD_FUNC_BODY, FIELD_FUNC_LINE)
            file_dict[KEY_FUNC_DETAIL] = list(query_set)
            logger.info("{0}: function count:{1}".format(self.__class__.__name__, len(file_dict[KEY_FUNC_DETAIL])))
            data_list.append(file_dict)

        return data_list

    def get_serializer_class(self):
        """
        Override the get_serializer_class() method
        :return:
        """

        if self.api_kind == API_KIND_DETAIL:
            return None
        return None


class CodeSearchView(GetDetailAPIView):
    """
    Search the special function from code class
    """

    def __init__(self):
        super(CodeSearchView, self).__init__()

    def get_queryset(self):
        """
        This function is override base get_queryset
        :return: queryset
        """

        data_list = []
        query_set = FunctionInfo.objects.filter(name=self.data_dict.get(FIELD_FUNC_NAME)).values(
            FIELD_FILE_NAME, FIELD_FUNC_NAME, FIELD_FUNC_PARAM, FIELD_FUNC_BODY, FIELD_FUNC_LINE)
        data_list = list(query_set)
        logger.info("{0}: function count:{1}".format(self.__class__.__name__, len(data_list)))

        return data_list
