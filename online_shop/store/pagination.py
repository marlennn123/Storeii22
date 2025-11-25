from rest_framework.pagination import PageNumberPagination

class ProductPagination(PageNumberPagination):
    page_size = 5


class CategoryPagination(PageNumberPagination):
    page_size = 8