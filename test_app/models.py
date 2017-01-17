# coding=utf-8
from __future__ import unicode_literals

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django_extensions.db.fields import CreationDateTimeField, ModificationDateTimeField
from timezone_field import TimeZoneField


class Account(models.Model):
    class Meta:
        verbose_name = _('Аккаунт')
        verbose_name_plural = _('Аккаунты')

    title = models.CharField(verbose_name=_('Название аккаунта'), max_length=255)
    shortname = models.CharField(verbose_name=_('4-х значное обозначение'), max_length=4)
    google_tracing = models.CharField(verbose_name=_(u'Google Universal Analytics ID'), max_length=100, null=True, blank=True)
    added = CreationDateTimeField(verbose_name=_('Дата создания'))
    updated = ModificationDateTimeField(verbose_name=_('Дата последнего изменения'))
    is_trial = models.BooleanField(default=False, verbose_name=_('Компания на триале'))
    trial_expires = models.DateField(null=True, blank=True)
    index_num = models.PositiveIntegerField(verbose_name=_('Номер индекса'), default=1)
    language = models.CharField(default="RU", max_length=2, choices=settings.LANGUAGES, verbose_name=_("Language"))

    def __unicode__(self):
        return self.title


class User(AbstractBaseUser, PermissionsMixin):

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        db_table = 'test_app_user'

    email = models.EmailField(
        verbose_name=u'Электронная почта',
        max_length=255,
        unique=True,
        db_index=True)

    account = models.ForeignKey('Account', null=True, blank=True, verbose_name=u'Связанный аккаунт')

    job_title = models.CharField(verbose_name=u'Должность', max_length=255, null=True, blank=True)
    username = models.CharField(verbose_name=u'Имя',  max_length=255, unique=True)
    gravatar = models.URLField(verbose_name=u'Gravatar', null=True, blank=True)
    is_active = models.BooleanField(default=True, verbose_name=u'Активен')
    is_admin = models.BooleanField(default=False, verbose_name=u'Админ')
    is_staff = models.BooleanField(default=False, verbose_name=u'Staff')

    phone = models.CharField(verbose_name=u'Телефон', max_length=15, null=True, blank=True)
    language = models.CharField(default="RU", null=True, blank=True,
                                max_length=2, choices=settings.LANGUAGES, verbose_name=_(u"Language"))

    timezone = TimeZoneField(default='Europe/Moscow', verbose_name=_(u"Timezone"))
    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __unicode__(self):
        return self.get_full_name()

    def save(self, *args, **kwargs):
        if not self.language and self.account:
            self.language = self.account.language
        super(User, self).save(*args, **kwargs)

    def get_full_name(self):
        return self.username or self.email

    def get_short_name(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

