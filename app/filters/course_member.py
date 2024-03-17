from django.db.models import F
from rest_framework import filters


class FilterStudents(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        sort_param = request.query_params.get("sort", None)
        if sort_param:
            field, order = sort_param.rsplit(".", 1)
            ordering = None
            sort_mappings = {
                "firstname": "user__first_name",
                "lastname": "user__last_name",
                "id": "user__id",
                "sections": "sections__name",
            }

            db_field = sort_mappings.get(field, None)
            if db_field:
                if order.lower() == "asc":
                    ordering = F(db_field).asc(nulls_last=True)
                elif order.lower() == "desc":
                    ordering = F(db_field).desc(nulls_last=True)

            return queryset.order_by(ordering) if ordering else queryset
        return queryset
