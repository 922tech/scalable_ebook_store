from rest_framework import pagination


class LimitedLimitOffsetPagination(pagination.LimitOffsetPagination):
    default_limit = 10
    max_limit = 20
