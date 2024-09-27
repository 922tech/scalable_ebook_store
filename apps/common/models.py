"""
This module includes the models that are supposed to be used by any other apps.
Do not write models that are related to other models in here.
"""

from django.db import models


class BaseQuerySet(models.QuerySet):
    """
    Every queryset in the application must be a subclass to this class.
    """

    def soft_delete(self):
        self.update(is_deleted=True)


class BaseManager(models.Manager.from_queryset(BaseQuerySet)):
    """
    Every custom managers in the application must be a subclass to class.
    """
    pass


class BaseModel(models.Model):
    """
    Every model in the application must be a subclass to this model.
    User is the only model that does not inherits from AbstractUser i.e. it cannot inherit from BaseModel
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    objects = BaseManager()

    class Meta:
        abstract = True
