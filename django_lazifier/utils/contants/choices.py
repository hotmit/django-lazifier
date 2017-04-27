from django.utils.translation import ugettext as _


GENDER_CHOICES = (
    ('male', _('Male')),
    ('female', _('Female')),
    ('other', _('Other')),
)


GENDER_ALL_CHOICES = (
    ('all', _('All')),
) + GENDER_CHOICES


STATUS_CHOICES = (
    ('active', _('Active')),
    ('inactive', _('Inactive')),
)


STATUS_ALL_CHOICES = (
    ('all', _('All')),
) + STATUS_CHOICES