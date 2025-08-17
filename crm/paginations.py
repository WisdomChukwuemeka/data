from rest_framework.pagination import CursorPagination

class CustomCursorPagination(CursorPagination):
    page_size = 4  # how many items per page
    ordering = '-id'  # MUST be unique + ordered

class CustomAdminEventPagination(CursorPagination):
    page_size = 8  # how many items per page
    ordering = '-id'  # MUST be unique + ordered


class CustomVideoPagination(CursorPagination):
    page_size = 3
    ordering = '-id'

class CustomMusicPagination(CursorPagination):
    page_size = 4
    ordering = '-id'