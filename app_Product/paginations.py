from rest_framework import pagination
from rest_framework.response import Response


class ProductPagination(pagination.PageNumberPagination):
    page_size = 24
    page_size_query_param = 'page_size'

    def get_paginated_response(self, data):
        return Response({
            'total': self.page.paginator.num_pages,
            'results': data
        })
