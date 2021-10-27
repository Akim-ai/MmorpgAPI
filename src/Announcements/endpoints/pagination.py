from rest_framework.pagination import PageNumberPagination


class PicturePagination(PageNumberPagination):
    page_size = 2
    page_query_description = 'page_size'
    max_page_size = 2
