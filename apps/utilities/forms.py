
from django import forms
from django.utils.translation import ugettext_lazy as _

from apps.admin.forms import AddChangeModelForm

from utils.django.widgets import AutosizedTextarea

from .models import Category, Utility


class CategoryAdminModelForm(AddChangeModelForm):

    disabled_fields = ('slug', )

    class Meta:
        widgets = {
            'description': AutosizedTextarea(),
        }


class UtilityAdminModelForm(AddChangeModelForm):

    class Meta:
        widgets = {
            'description': AutosizedTextarea(),
        }
