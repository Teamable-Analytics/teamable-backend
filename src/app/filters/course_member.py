from django.db.models import F, Q
from rest_framework import filters


class FilterStudents(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        queryset = self.search_queryset(request, queryset, view)
        queryset = self.sort_queryset(request, queryset, view)
        queryset = self.filter_queryset_by_section(request, queryset, view)
        return queryset

    def sort_queryset(self, request, queryset, view):
        sort_param = request.query_params.get("sort", None)
        if sort_param:
            field, order = sort_param.rsplit(".")
            ordering = None
            sort_mappings = {
                "first_name": "first_name",
                "last_name": "last_name",
                "id": "sis_user_id",
            }

            db_field = sort_mappings.get(field, None)
            if db_field is not None:
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
                Q(sis_user_id__icontains=str(search_param)),
                Q(first_name__icontains=str(search_param)),
                Q(last_name__icontains=str(search_param)),
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
