
from django.contrib.auth import authenticate
from django.utils.translation import ugettext_lazy as _
from django import forms
from django.utils.html import mark_safe


class LoginForm(forms.Form):
    """ """

    credential = forms.CharField(
        label=_('Email or username'),
        widget=forms.TextInput(attrs={
            'placeholder': _('Enter username or email'),
            'class': 'form-control',
            'autofocus': '',
        }),
        strip=True,
        help_text=_('Field is case-sensetive'),
    )
    password = forms.CharField(
        label=_('Password'),
        widget=forms.PasswordInput(attrs={
            'placeholder': _('Enter password'),
            'class': 'form-control',
        }),
        strip=False,
    )

    error_messages = {
        'invalid_login': _('Please enter a correct credentials for login.'),
        'inactive': _('This user is inactive.'),
    }

    def __init__(self, *args, **kwargs):

        # for keeping trying authentication of an user
        self.user = None

        super().__init__(*args, **kwargs)

    def clean(self):

        credential = self.cleaned_data.get('credential')
        password = self.cleaned_data.get('password')

        if credential and password:
            user = authenticate(credential=credential, password=password)

            if user is None:
                raise forms.ValidationError(self.error_messages['invalid_login'], code='invalid_login')

            if not user.is_active:
                raise forms.ValidationError(self.error_messages['inactive'], code='inactive')

            # keep a active and authenticated of an user
            self.user = user

        return self.cleaned_data

    def get_user(self):
        """ """

        return self.user


class LogoutForm(forms.Form):

    pass


class ReadOnlyWidget(forms.Widget):

    def render(self, name, value, attrs=None):
        return value


class AddChangeModelForm(forms.ModelForm):

    fields_without_classes = tuple()
    disabled_fields = tuple()
    fields_placeholders = tuple()
    addons = dict()

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        if self.fields_without_classes is not '__all__':

            for name, field in self.fields.items():

                if name in ['name']:
                # if name in self.model_admin.get_readonly_fields():
                    field.widget = ReadOnlyWidget()
                    continue

                if name in self.fields_without_classes:
                    continue

                classes = getattr(field.widget.attrs, 'class', [])
                classes.append('form-control')

                field.widget.attrs['class'] = ' '.join(classes)

                if name in self.disabled_fields:
                    field.disabled = True

                verbose_name = self.Meta.model._meta.get_field(name).verbose_name

                field.widget.attrs['placeholder'] = 'Enter {}'.format(verbose_name.lower())

                field.help_text = self._get_help_text_to_field(field)

    @staticmethod
    def _get_help_text_to_field(field):

        help_text = field.help_text + '<br />' if field.help_text else ''

        min_length = getattr(field, 'min_length', -1)
        max_length = getattr(field, 'max_length', -1)

        if (min_length == -1 and max_length == -1) or (min_length is None and max_length is None):
            length_help_text = ''
        # elif min_length is not None and max_length is None:
        #     length_help_text = 'Length from {} characters.'.format(min_length)
        elif min_length is None and max_length > 1:
            length_help_text = 'Length not more then {} characters.'.format(max_length)
        else:
            length_help_text = 'Length from {} to {} characters.'.format(min_length, max_length)

        help_text = mark_safe(help_text + length_help_text)

        return help_text


class AddChangeDisplayForm:

    def __init__(self, form, fieldsets):
        self.fieldsets = fieldsets
        self.form = form

    def __iter__(self):

        for name, options in self.fieldsets:
            yield FieldSet(self.form, name, **options)


class FieldSet:

    def __init__(self, form, name, fields, classes=None, description=None):
        self.form = form
        self.name = name
        self.fields = fields
        self.classes = classes
        self.description = description

    def __iter__(self):
        for field in self.fields:
            yield FieldSetLine(self.form, field)


class FieldSetLine:

    def __init__(self, form, field):
        self.field = form[field]

    def __str__(self):
        return str(self.field)

    def label_tag(self):

        # override label_tag on BoundField
        return self.field.label_tag(attrs={'class': 'col-xs-2 control-label'})