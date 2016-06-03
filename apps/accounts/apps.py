
# import uuid

# from django.core.signals import request_finished
# from django.dispatch import receiver
# from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _
from django.apps import AppConfig


class AccountsConfig(AppConfig):
    name = 'apps.accounts'
    verbose_name = _('Accounts')