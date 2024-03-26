from django.db.models import F
from django.db.models import Q
from rest_framework import filters
from django.db.models import Value, CharField
from django.db.models.functions import Concat


class FilterStudents(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        queryset = self.search_queryset(request, queryset, view)
        queryset = self.sort_queryset(request, queryset, view)
        queryset = self.filter_queryset_by_section(request, queryset, view)
        return queryset

    def sort_queryset(self, request, queryset, view):
        sort_param = request.query_params.get("sort", None)
        if sort_param:
            field, order = sort_param.rsplit(".", 1)
            ordering = None
            sort_mappings = {
                "firstname": "user__first_name",
                "lastname": "user__last_name",
                "id": "user__id",
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
        search_param = request.query_params.get("title", None)

        if search_param:
            search_mappings = {
                "id": ("user__id", str),
            }
            queries = []
            for field, (query_param, expected_type) in search_mappings.items():
                try:
                    if expected_type == str:
                        queries.append(
                            Q(**{query_param + "__icontains": str(search_param)})
                        )
                except ValueError:
                    continue
            queryset = queryset.annotate(
                full_name=Concat(
                    "user__first_name",
                    Value(" "),
                    "user__last_name",
                    output_field=CharField(),
                )
            )
            queries.append(Q(full_name__icontains=str(search_param)))
            query = Q()
            for condition in queries:
                query |= condition

            queryset = queryset.filter(query)
        return queryset

    def filter_queryset_by_section(self, request, queryset, view):
        sections = request.query_params.get("sections", None)
        sections = sections.split(".") if sections else None
        query = Q()

        if sections:
            for section in sections:
                query |= Q(sections=section)

        queryset = queryset.filter(query).distinct()
        return queryset
