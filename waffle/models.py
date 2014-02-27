try:
    from django.utils import timezone as datetime
except ImportError:
    from datetime import datetime

from django.contrib.auth.models import Group
from django.db import models

from waffle.compat import User


class Flag(models.Model):
    """A feature flag.

    Flags are active (or not) on a per-request basis.

    """
    name = models.CharField(max_length=100, unique=True,
                            help_text='The human/computer readable name.')
    everyone = models.NullBooleanField(blank=True, help_text=(
        'Flip this flag on (Yes) or off (No) for everyone, overriding all '
        'other settings. Leave as Unknown to use normally.'))
    percent = models.DecimalField(max_digits=3, decimal_places=1, null=True,
                                  blank=True, help_text=(
        'A number between 0.0 and 99.9 to indicate a percentage of users for '
        'whom this flag will be active.'))
    testing = models.BooleanField(default=False, help_text=(
        'Allow this flag to be set for a session for user testing.'))
    superusers = models.BooleanField(default=True, help_text=(
        'Flag always active for superusers?'))
    staff = models.BooleanField(default=False, help_text=(
        'Flag always active for staff?'))
    authenticated = models.BooleanField(default=False, help_text=(
        'Flag always active for authenticate users?'))
    languages = models.TextField(blank=True, default='', help_text=(
        'Activate this flag for users with one of these languages (comma '
        'separated list)'))
    rollout = models.BooleanField(default=False, help_text=(
        'Activate roll-out mode?'))
    note = models.TextField(blank=True, help_text=(
        'Note where this Flag is used.'))
    created = models.DateTimeField(default=datetime.now, db_index=True,
        help_text=('Date when this Flag was created.'))
    modified = models.DateTimeField(default=datetime.now, help_text=(
        'Date when this Flag was last modified.'))

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.modified = datetime.now()
        super(Flag, self).save(*args, **kwargs)


class Switch(models.Model):
    """A feature switch.

    Switches are active, or inactive, globally.

    """
    name = models.CharField(max_length=100, unique=True,
                            help_text='The human/computer readable name.',
                            db_index=True)
    active = models.BooleanField(default=False, help_text=(
        'Is this flag active?'), db_index=True)
    note = models.TextField(blank=True, help_text=(
        'Note where this Switch is used.'), db_index=True)
    created = models.DateTimeField(default=datetime.now, db_index=True,
        help_text=('Date when this Switch was created.'))
    modified = models.DateTimeField(default=datetime.now, help_text=(
        'Date when this Switch was last modified.'), db_index=True)

    def __unicode__(self):
        return u'%s: %s' % (self.name, 'on' if self.active else 'off')

    def save(self, *args, **kwargs):
        self.modified = datetime.now()
        super(Switch, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Switches'


class Sample(models.Model):
    """A sample is true some percentage of the time, but is not connected
    to users or requests.
    """
    name = models.CharField(max_length=100, unique=True,
                            help_text='The human/computer readable name.')
    percent = models.DecimalField(max_digits=4, decimal_places=1, help_text=(
        'A number between 0.0 and 100.0 to indicate a percentage of the time '
        'this sample will be active.'))
    note = models.TextField(blank=True, help_text=(
        'Note where this Sample is used.'))
    created = models.DateTimeField(default=datetime.now, db_index=True,
        help_text=('Date when this Sample was created.'))
    modified = models.DateTimeField(default=datetime.now, help_text=(
        'Date when this Sample was last modified.'))

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.modified = datetime.now()
        super(Sample, self).save(*args, **kwargs)
