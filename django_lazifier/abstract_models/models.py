from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings


class TimeStampQuerySet(models.QuerySet):
    def created_between(self, start, end):
        return self.filter(created__range=(start, end))

    def modified_between(self, start, end):
        return self.filter(modified__range=(start, end))


class EnabledQuerySet(models.QuerySet):
    def enabled(self):
        return self.filter(enabled=True)

    def disabled(self):
        return self.filter(enabled=False)


class ActiveQuerySet(models.QuerySet):
    def active_records(self):
        return self.filter(is_active=True)

    def inactive_records(self):
        return self.filter(is_active=False)


class OwnerQuerySet(models.QuerySet):
    def by_owner(self, owner):
        if type(owner) is not int:
            owner = getattr(owner, 'id')
        return self.filter(owner_id=owner)


class BaseQuerySet(TimeStampQuerySet, EnabledQuerySet, ActiveQuerySet, OwnerQuerySet):
    def active_by_owner(self, owner):
        filter = self.active_records()
        return filter.by_owner(owner)


class TimestampModel(models.Model):
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('created'))
    modified = models.DateTimeField(auto_now=True, verbose_name=_('last modified'))

    objects = BaseQuerySet.as_manager()

    class Meta:
        abstract = True


class EnabledModel(models.Model):
    enabled = models.BooleanField(default=True, verbose_name=_('enabled'))

    objects = BaseQuerySet.as_manager()

    class Meta:
        abstract = True


class ActiveStatusModel(models.Model):
    is_active = models.BooleanField(default=True, verbose_name=_('is active'))

    objects = BaseQuerySet.as_manager()

    class Meta:
        abstract = True


class OwnerModel(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, verbose_name=_('owner'), editable=False)

    objects = BaseQuerySet.as_manager()

    class Meta:
        abstract = True

    def save(self, *args, owner=None, **kwargs):
        if owner is not None:
            self.owner = owner
        return super().save(*args, **kwargs)
