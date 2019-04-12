# -*- coding: utf-8 -*-

from rest_framework.generics import GenericAPIView
from django.http import QueryDict
from django.core import serializers
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from logging import getLogger

logger = getLogger('django')

"""API Kind Code"""
API_KIND_CREATE = 0
API_KIND_DETAIL = 1
API_KIND_UPDATE = 2
API_KIND_DELETE = 3

"""API Result Code"""
SUCCESS = 0
PARAMETER_ERROR = 101
CONNECTION_ERROR = 201
CREATE_ERROR = 202
UPDATE_ERROR = 203
READ_ERROR = 204
DELETE_ERROR = 205

EXCEPTION_EXIT = -1

""" Dict key words"""
KEY_RESULT = "result"
KEY_DATA_LIST = "data"


class BaseAPIView(GenericAPIView):
    """
    Basic class for server API
    """

    def __init__(self):
        super(BaseAPIView, self).__init__()
        self.api_kind = None
        self.result_dict = {KEY_RESULT: SUCCESS}
        self.data_dict = {}
        self.data_ret = []

    def api_response(self, serialized_data=None, status_code=status.HTTP_200_OK):
        """
        This function is used to generate response for API.
        :param serialized_data:
        :param status_code:
        :return: Response
        """
        if serialized_data is not None:
            self.result_dict[KEY_DATA_LIST] = serialized_data
        return Response(data=self.result_dict, status=status_code)

    def set_api_result(self):
        """
        This function is used to set result code
        :return:
        """
        if self.api_kind == API_KIND_CREATE:
            self.result_dict[KEY_RESULT] = CREATE_ERROR
        elif self.api_kind == API_KIND_DETAIL:
            self.result_dict[KEY_RESULT] = READ_ERROR
        elif self.api_kind == API_KIND_UPDATE:
            self.result_dict[KEY_RESULT] = UPDATE_ERROR
        elif self.api_kind == API_KIND_DELETE:
            self.result_dict[KEY_RESULT] = DELETE_ERROR

    def get_parameter_dic(self, request):
        """
        This function is used to get request data to dict
        :param request: Django REST framework raw request
        :return: True or False
        """

        result = False

        try:
            if not isinstance(request, Request):
                return result

            query_params = request.query_params
            if isinstance(query_params, QueryDict):
                query_params = query_params.dict()
            result_data = request.data
            if isinstance(result_data, QueryDict):
                result_data = result_data.dict()

            if query_params != {}:
                self.data_dict = query_params.get('params', query_params)
            else:
                self.data_dict = result_data

            # convert string value
            if isinstance(self.data_dict, str):
                self.data_dict = eval(self.data_dict)
            elif isinstance(self.data_dict, dict):
                for key in self.data_dict:
                    if isinstance(self.data_dict[key], str) and self.data_dict[key].startswith(('[', '{')):
                        self.data_dict[key] = eval(self.data_dict[key])

            logger.info("{0}: params data:{1}".format(self.__class__.__name__, self.data_dict))
        except Exception as e:
            logger.info("{0}: parameter error:{1}".format(self.__class__.__name__, repr(e)))
        else:
            result = True
        return result


class CreateBaseAPIView(BaseAPIView):
    """
    Basic Create API, only support 'GET' method
    """

    def get(self, request):
        """
        API 'GET' method for database 'read' operation
        Need to override get_queryset() function when extends
        :param request:
        :return:
        """

        self.api_kind = API_KIND_CREATE

        if self.get_parameter_dic(request):
            # todo aynalize code & insert to database
            if self.do_aynalize():
                logger.info("{0}: do aynalise result:{1}".format(self.__class__.__name__, self.data_ret))
                response = self.api_response(self.data_ret, status_code=status.HTTP_200_OK)
            else:
                self.set_api_result()
                response = self.api_response(status_code=status.HTTP_200_OK)
        else:
            self.result_dict[KEY_RESULT] = PARAMETER_ERROR
            response = self.api_response(status_code=status.HTTP_400_BAD_REQUEST)
        logger.info("{0}: response:{1}".format(self.__class__.__name__, response))

        return response

    def do_aynalize(self):
        result = True
        logger.info("{0}: do aynalise result:{1}".format(self.__class__.__name__, result))
        return result


class GetDetailAPIView(BaseAPIView):
    """
    Basic Detail API, only support 'GET' method
    """

    def get(self, request):
        """
        API 'GET' method for database 'read' operation
        Need to override get_queryset() function when extends
        :param request:
        :return:
        """

        self.api_kind = API_KIND_DETAIL

        if self.get_parameter_dic(request):
            # todo get data
            queryset = self.get_queryset()
            response = self.api_response(queryset, status_code=status.HTTP_200_OK)
        else:
            self.result_dict[KEY_RESULT] = PARAMETER_ERROR
            response = self.api_response(status_code=status.HTTP_400_BAD_REQUEST)
        logger.info("{0}: response:{1}".format(self.__class__.__name__, response))

        return response
