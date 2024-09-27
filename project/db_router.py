from typing import Any, Literal, Optional
from django.db.models.base import ModelBase


class DBRouter:
    def __init__(self, app_labels: list, db_name: str):
        self.app_labels = app_labels
        self.db_name = db_name

    def db_for_read(self, model: ModelBase, **hints) -> str | None:
        if model._meta.app_label in self.app_labels:
            return self.db_name
        return None

    def db_for_write(self, model: ModelBase, **hints) -> str | None:
        if model._meta.app_label in self.app_labels:
            return self.db_name
        return None

    def allow_relation(self, obj1, obj2, **hints) -> None | Literal[True]:
        if obj1._meta.app_label in self.app_labels or obj2._meta.app_label in self.app_labels:
            return True
        return None

    def allow_migrate(self, db: str, app_label: str, model_name: Optional[str | None] = None, **hints) -> bool | None:
        if app_label in self.app_labels:
            return db == self.db_name
        return None
