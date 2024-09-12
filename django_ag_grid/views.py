import json
from django.views.generic.list import ListView
from django.http import JsonResponse
from django.db.models import Q, QuerySet, FileField, ImageField


class BaseAGGridView(ListView):
    column_defs = []

    def apply_filters(self, filters: dict, queryset: QuerySet) -> QuerySet:
        q_objects = Q()

        for key, filter_info in filters.items():
            filter_type = filter_info.get("type")
            filter_value = filter_info.get("filter")

            if filter_type == "contains":
                lookup = f"{key}__icontains"
                q_objects &= Q(**{lookup: filter_value})
            elif filter_type == "equals":
                lookup = f"{key}__exact"
                q_objects &= Q(**{lookup: filter_value})
            elif filter_type == "notEqual":
                lookup = f"{key}__exact"
                q_objects &= ~Q(**{lookup: filter_value})
            elif filter_type == "greaterThan":
                lookup = f"{key}__gt"
                q_objects &= Q(**{lookup: filter_value})
            elif filter_type == "lessThan":
                lookup = f"{key}__lt"
                q_objects &= Q(**{lookup: filter_value})

        return queryset.filter(q_objects)

    def apply_sort(self, sort: list, queryset: QuerySet) -> QuerySet:
        sort_fields = []

        for sort_object in sort:
            col_id = sort_object["colId"]
            sort_order = sort_object["sort"]
            if sort_order == "asc":
                sort_fields.append(col_id)
            elif sort_order == "desc":
                sort_fields.append(f"-{col_id}")

        if sort_fields:
            queryset = queryset.order_by(*sort_fields)

        return queryset

    def get_queryset(self):
        queryset = super().get_queryset()
        filter_params = self.request.GET.get("filter", None)
        sort_params = self.request.GET.get("sort", None)

        if filter_params:
            queryset = self.apply_filters(json.loads(filter_params), queryset)
        if sort_params:
            queryset = self.apply_sort(json.loads(sort_params), queryset)
        return queryset

    def convert_file_fields(self, queryset):
        """
        Converte campos de arquivos/imagens em URLs.
        """
        rows = []
        for row in queryset:
            cols = {}
            for col_def in self.column_defs:
                field_name = col_def['field']
                field = self.model._meta.get_field(field_name)

                # Se o campo for do tipo arquivo ou imagem, converte para URL

                if isinstance(field, (FileField, ImageField)) and row.get(field_name):
                    cols[field_name] = row[field_name].url
                else:
                    cols[field_name] = row[field_name]
            rows.append(cols)
        return rows

    def get(self, request, *args, **kwargs):
        start_row = int(request.GET.get("startRow", 0))
        end_row = int(request.GET.get("endRow", 100))
        queryset = self.get_queryset()
        total_rows = queryset.count()
        queryset = queryset[start_row:end_row]

        rows = queryset.only(
                *[col['field'] for col in self.column_defs]
            ) if self.column_defs else queryset

        rows = self.convert_file_fields(rows)
        return JsonResponse({"rows": rows, "totalRows": total_rows})
