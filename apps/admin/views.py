
from django.core.exceptions import ImproperlyConfigured
from django import forms
from django.utils.html import format_html
from django.db.models import NullBooleanField, BooleanField
from django.apps import apps
from django.db.models.fields.reverse_related import ManyToOneRel
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.views import generic
from django.contrib.auth import login, logout
from django.utils.text import capfirst, force_text

from utils.django.views_mixins import ContextTitleMixin

from .forms import LoginForm, AddModelForm
from .descriptors import SiteAdminStrictDescriptor, ModelAdminStrictDescriptor
from .views_mixins import SiteAdminMixin, SiteModelAdminMixin, SiteAppAdminMixin


class IndexView(SiteAdminMixin, generic.TemplateView):

    template_name = 'admin/admin/index.html'
    title = _('Index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class LoginView(ContextTitleMixin, generic.FormView):

    template_name = 'admin/admin/login.html'
    form_class = LoginForm
    title = _('Login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):

        login(self.request, form.get_user())

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('admin:index')


class LogoutView(generic.RedirectView):

    pattern_name = 'admin:login'
    permament = False

    def get_redirect_url(self, *args, **kwargs):

        logout(self.request)

        return super().get_redirect_url(*args, **kwargs)


class PasswordChangeView(generic.TemplateView):

    template_name = 'admin/admin/password_change.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update(self.site_admin.each_context(self.request))

        context['title'] = _('Password change')

        return context


class PasswordChangeDoneView(generic.TemplateView):

    pass


class ChangeListView(SiteModelAdminMixin, generic.ListView):

    template_name = 'admin/admin/changelist.html'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.default_styles = {
            'align': 'left',
        }

    def get_queryset(self):

        return self.model_admin.get_queryset(self.request)

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        model_meta = self.model_admin.model._meta

        context['title'] = _('Select {} to change').format(model_meta.verbose_name_plural.lower())

        context['model_meta'] = model_meta
        context['app_index_url'] = reverse('admin:{}_index'.format(model_meta.app_label))

        context['has_add_permission'] = self.model_admin.has_add_permission(self.request)
        context['add_url'] = reverse('admin:{}_{}_add'.format(model_meta.app_label, model_meta.model_name))

        context['list_display_with_styles'] = self.get_list_display_with_styles()

        context['list_values_with_styles'] = self.get_list_values_with_styles()

        return context

    @property
    def list_display_styles_by_column(self):

        columns_with_styles = {}

        styles_by_column = {
            column: styles
            for columns, styles in self.model_admin.get_list_display_styles()
            for column in columns
        }

        global_styles = styles_by_column.pop('__all__') if '__all__' in styles_by_column else dict()

        list_display_dict = dict.fromkeys(self.model_admin.get_list_display(), {})

        for column, styles in list_display_dict.items():

            value = self.default_styles.copy()
            value.update(global_styles)
            value.update(styles_by_column.get(column, {}))
            columns_with_styles[column] = value

        return columns_with_styles

    def get_list_values_with_styles(self):

        list_values_with_styles = list()

        for obj in self.get_queryset():

            values = list()
            for field_or_method in self.model_admin.get_list_display():

                if hasattr(obj, field_or_method):
                    value = getattr(obj, field_or_method)
                elif hasattr(self.model_admin, field_or_method):
                    model_admin_method = getattr(self.model_admin, field_or_method)
                    value = model_admin_method(obj)

                fieldnames = [field.name for field in self.model_admin.model._meta.get_fields()]

                # if it is not field, then it is method
                if callable(value):
                    value = value()

                elif field_or_method in fieldnames:

                    field = self.model_admin.model._meta.get_field(field_or_method)

                    if field.choices:
                        value = getattr(obj, 'get_{}_display'.format(field_or_method))()

                    if isinstance(field, (NullBooleanField, BooleanField)):

                        if value is True:
                            bootstap_class = 'ok-sign'
                            color = 'rgb(0, 255, 0)'
                        elif value is False:
                            bootstap_class = 'remove-sign'
                            color = 'rgb(255, 0, 0)'
                        elif value is None:
                            bootstap_class = 'question-sign'
                            color = 'rgb(0, 0, 0)'

                        value = format_html(
                            '<span class="glyphicon glyphicon-{}" style="color: {}"></span>',
                            bootstap_class, color
                        )

                if value is None:
                    value = self.site_admin.empty_value_display

                values.append((value, self.list_display_styles_by_column[field_or_method]))

            row_color = self.get_row_color(obj)

            admin_url = reverse('admin:{}_{}_change'.format(
                self.model_admin.model._meta.app_label,
                self.model_admin.model._meta.model_name,
            ), args=(obj.pk, ))

            list_values_with_styles.append((row_color, admin_url, values))
        return list_values_with_styles

    def get_list_display_with_styles(self):

        list_display = self.model_admin.get_list_display()

        new_list_display = list()

        for name_attr_display in list_display:

            # made also __all__
            if name_attr_display == '__str__':

                attr_display = self.model_admin.model._meta.verbose_name

            else:

                if hasattr(self.model_admin.model, name_attr_display):
                    attr_display = getattr(self.model_admin.model, name_attr_display)
                elif hasattr(self.model_admin, name_attr_display):
                    attr_display = getattr(self.model_admin, name_attr_display)
                else:
                    raise AttributeError(
                        'Either no model or model admin has no attribute {}'.format(
                            name_attr_display
                        )
                    )

                if callable(attr_display):

                    if hasattr(attr_display, 'short_description'):
                        attr_display = force_text(attr_display.short_description)
                    else:
                        attr_display = attr_display.__name__.replace('_', ' ')
                        attr_display = force_text(attr_display)
                        attr_display = capfirst(attr_display)

                elif isinstance(attr_display, property):

                    attr_display = attr_display.fget.__name__.replace('_', ' ')
                    attr_display = force_text(attr_display)
                    attr_display = capfirst(attr_display)

                else:

                    field = self.model_admin.model._meta.get_field(name_attr_display)

                    if isinstance(field, ManyToOneRel):
                        raise TypeError(
                            'Does not support for field ({}) with type ManyToOneRel.'.format(field.name)
                        )

                    attr_display = field.verbose_name

            new_list_display.append((attr_display, self.list_display_styles_by_column[name_attr_display]))

        return new_list_display

    def get_row_color(self, obj):

        colored_rows_by = self.model_admin.get_colored_rows_by()

        row_color = None
        if hasattr(self.model_admin, colored_rows_by):

            colored_rows_by = getattr(self.model_admin, colored_rows_by)
            if callable(colored_rows_by):
                row_color = colored_rows_by(obj)

        return row_color


class AddView(SiteModelAdminMixin, generic.CreateView):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.model_meta = self.model_admin.model._meta

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['title'] = _('Add {}').format(self.model_meta.verbose_name.lower())

        context['model_meta'] = self.model_meta

        context['app_index_url'] = reverse('admin:{}_index'.format(self.model_meta.app_label))

        return context

    def get_template_names(self):

        return [
            '{}/admin/{}/add_form.html'.format(self.model_meta.app_label, self.model_meta.model_name),
            '{}/admin/add_form.html'.format(self.model_meta.app_label),
            'admin/admin/add_form.html',
        ]

    def get_queryset(self):

        return self.model_admin.model._default_manager

    def get_form_class(self):

        form = getattr(self.model_admin, 'form', AddModelForm)

        return forms.models.modelform_factory(
            self.model_admin.model, fields='__all__', form=form
        )


class ChangeView(SiteModelAdminMixin, generic.UpdateView):

    pass


class AppIndexView(SiteAppAdminMixin, generic.TemplateView):

    template_name = 'admin/admin/app_index.html'

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context['title'] = self.app_config.verbose_name
        context['app_name'] = self.app_config.verbose_name
        context['app_models_info'] = self.get_app_models_info()
        context['reports_url'] = reverse('admin:{}_reports'.format(self.app_config.label))
        context['statistics_url'] = reverse('admin:{}_statistics'.format(self.app_config.label))

        return context

    def get_app_models_info(self):

        info = list()
        for model in self.app_config.get_models():

            info.append((
                force_text(model._meta.verbose_name),
                reverse('admin:{}_{}_changelist'.format(model._meta.app_label, model._meta.model_name)),
                model._default_manager.count(),
            ))

        info.sort(key=lambda x: x[0].lower())

        return info


class AppReportView(SiteAppAdminMixin, generic.TemplateView):

    template_name = 'admin/admin/reports.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['title'] = _('{} - Reports ').format(self.app_config.verbose_name)

        context['app_name'] = self.app_config.verbose_name
        context['app_index_url'] = reverse('admin:{}_index'.format(self.app_config.label))

        return context


class AppStatisticsView(SiteAppAdminMixin, generic.TemplateView):

    template_name = 'admin/admin/statistics.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['title'] = _('{} - Statistics ').format(self.app_config.verbose_name)

        context['app_name'] = self.app_config.verbose_name
        context['app_index_url'] = reverse('admin:{}_index'.format(self.app_config.label))

        return context


class HistoryView(SiteModelAdminMixin, generic.DetailView):

    pass


class DeleteView(SiteModelAdminMixin, generic.DeleteView):

    pass


class ExportView(generic.View):

    pass


class ImportPreviewView(generic.View):

    pass


class ImportView(generic.View):

    pass


class SettingsView(SiteAdminMixin, generic.TemplateView):

    template_name = ''

    # constants
