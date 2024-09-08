from django.db.models import F, Func, Q, Value
from django.db.models.functions import Substr
from rest_framework import filters

from teamable.settings import DEBUG


class FilterStudents(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        queryset = self.search_queryset(request, queryset, view)
        queryset = self.sort_queryset(request, queryset, view)
        queryset = self.filter_queryset_by_section(request, queryset, view)
        return queryset

    def sort_queryset(self, request, queryset, view):
        sort_param = request.query_params.get("sort", None)
        if sort_param:
            """
            To create temporary fields for first and last name to enable sorting by them individually.
            SQLite is used for local development, and has the INSTR function for this.
            PostgresSQL is used on prod and has the POSITION function for this
            """
            function_name = "INSTR" if DEBUG else "POSITION"
            queryset = queryset.annotate(
                first_space_position=Func(
                    F("name"), Value(" "), function=function_name
                ),
                first_name=Substr(F("name"), 1, F("first_space_position") - 1),
                last_name=Substr(F("name"), F("first_space_position") + 1),
            ).order_by("first_name")

            field, order = sort_param.rsplit(".")
            ordering = None
            sort_mappings = {
                "firstName": "first_name",
                "lastName": "last_name",
                "id": "lms_id",
            }

            db_field = sort_mappings.get(field, None)
            if db_field:
                if order.lower() == "asc":
                    ordering = F(db_field).asc(nulls_last=True)
                elif order.lower() == "desc":
                    ordering = F(db_field).desc(nulls_last=True)
            queryset = queryset.order_by(ordering)
        return queryset

    def search_queryset(self, request, queryset, view):
        search_param = request.query_params.get("search", None)

        if search_param:
            queries = [
                Q(lms_id__icontains=str(search_param)),
                Q(name__icontains=str(search_param)),
            ]
            query = Q()
            for condition in queries:
                query |= condition

            queryset = queryset.filter(query)
        return queryset

    def filter_queryset_by_section(self, request, queryset, view):
        sections = request.query_params.get("sections", None)
        sections = sections.split(",") if sections else None
        query = Q()

        if sections:
            query |= Q(sections__in=sections)

        queryset = queryset.filter(query).distinct()
        return queryset
