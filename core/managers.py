from django.db import models

class BaseQuerySet(models.QuerySet):
    def values_by_col_name(self, offset=None, limit=None):
        col_map = {
            field.name: field.db_column or field.attname
            for field in self.model._meta.fields
        }
        queryset = self.values(*col_map.keys())
        if offset is not None and limit is not None:
            queryset = queryset[offset: offset + limit]
        return [
            {col_map[k]: v for k, v in record.items()}
            for record in queryset
        ]
        

class BaseManager(models.Manager):
    def get_queryset(self):
        return BaseQuerySet(self.model, using=self._db)

    def values_by_col_name(self, offset=None, limit=None):
        return self.get_queryset().values_by_col_name(offset, limit)