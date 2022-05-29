from rest_framework import pagination
from rest_framework.response import Response
from rest_framework.utils.urls import remove_query_param, replace_query_param


class PricePagination(pagination.LimitOffsetPagination):
    def get_paginated_response(self, data):
        # build current url
        url = self.request.build_absolute_uri()
        base_url = replace_query_param(url, self.limit_query_param, self.limit)
        return Response({
            'url': base_url,
            'next': self.get_next_link(),
            'count': self.count,
            'data': data
        })
