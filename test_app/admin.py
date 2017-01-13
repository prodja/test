# coding=utf-8
from __future__ import unicode_literals
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib import messages
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.contrib.auth import login

from test_app.models import Account, User
from django.contrib.auth.models import Group


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    pass


@admin.register(User)
class UserAdmin(UserAdmin):

    # ЗАЙТИ ПОД ПОЛЬЗОВАТЕЛЕМ get_urls
    def get_urls(self):
        urls = super(UserAdmin, self).get_urls()

        my_urls = [
            url(r'^login_as_user/$', self.admin_site.admin_view(self.login_as, cacheable=False), name='login_as')
        ]

        return my_urls+urls

    form = UserChangeForm
    add_form = UserCreationForm
    list_display = ('username', 'account', 'login_as_user')
    list_filter = ('is_admin', )

    # ЗАЙТИ ПОД ПОЛЬЗОВАТЕЛЕМ login_as
    def login_as(self, request):

        try:
            user = User.objects.get(pk=request.GET.get('id'))
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)
            return redirect('index')
        except User.DoesNotExist:
            messages.error(request, u'Пользователь не существует')
            return redirect('admin:account_user_changelist')

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Персональная информация', {'fields': ('account', 'username', 'job_title', 'language')}),
        ('Важные даты', {'fields': ('last_login',)}),
    )

    readonly_fields = ['last_login']

    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()

    # ЗАЙТИ ПОД ПОЛЬЗОВАТЕЛЕМ login_as_user
    def login_as_user(self, obj):
        return u"<a href='%s?id=%s' >Зайти под пользователем</a>" % (reverse('admin:login_as'), obj.id)

    # ЗАЙТИ ПОД ПОЛЬЗОВАТЕЛЕМ short_description, allow_tags
    login_as_user.short_description = u'Зайти под пользователем'
    login_as_user.allow_tags = True

admin.site.unregister(Group)
