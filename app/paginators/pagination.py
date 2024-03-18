from rest_framework.pagination import PageNumberPagination


class ExamplePagination(PageNumberPagination):
    # just a class to set up pagination for the Students CourseMembers view set.
    page_size = 5
    page_size_query_param = "per_page"
    max_page_size = 100
