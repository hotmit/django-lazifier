from django.db import models
from django.utils.translation import ugettext as _
from django.conf import settings


GENDERS = (
    ('male', _('Male')),
    ('female', _('Female')),
)


class DemoModel(models.Model):
    name = models.CharField(max_length=40, verbose_name=_('name'))
    description = models.TextField(blank=True, verbose_name=_('description'))
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, verbose_name=_('user'))
    gender = models.CharField(null=False, blank=False, max_length=10,
                              choices=GENDERS, default='female', verbose_name=_('gender'))
    pins = models.PositiveIntegerField(null=True, blank=True, verbose_name=_('pin'))

    modified = models.DateTimeField(auto_now=True, verbose_name=_("modified timestamped"))

    class Meta:
        db_table = 'dt_demo_model'
        verbose_name = _('Data Table Demo')
        permissions = (
            ('view_demoapp', _('View Demo App')),
            ('update_demoapp', _('Update Demo App')),
            ('delete_demoapp', _('Delete Demo App')),
            ('manage_demoapp', _('Manage Demo App')),
        )
