
from django.contrib.contenttypes.fields import GenericRelation
from django.core.urlresolvers import reverse
from django.core.validators import MinLengthValidator
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.conf import settings

from autoslug import AutoSlugField

from apps.app_generic_models.models import UserComment_Generic, UserOpinion_Generic
from apps.app_tags.models import Tag
from mylabour.models import TimeStampedModel
from mylabour.utils import CHOICES_LEXERS


class Snippet(TimeStampedModel):
    """

    """

    title = models.CharField(
        _('Title'), max_length=200, unique=True, validators=[MinLengthValidator(settings.MIN_LENGTH_FOR_NAME_OR_TITLE_OBJECT)]
    )
    slug = AutoSlugField(_('Slug'), populate_from='title', always_update=True, unique=True, allow_unicode=True)
    lexer = models.CharField(_('Lexer of code'), max_length=50, choices=CHOICES_LEXERS)
    description = models.TextField(_('Decription'))
    code = models.TextField(_('Code'))
    views = models.IntegerField(_('Count views'), default=0, editable=False)
    tags = models.ManyToManyField(
        Tag,
        verbose_name=_('Tags'),
        related_name='snippets',
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('Author'),
        related_name='snippets',
        on_delete=models.DO_NOTHING,
        limit_choices_to={'is_active': True},
    )
    opinions = GenericRelation(UserOpinion_Generic)
    comments = GenericRelation(UserComment_Generic)

    class Meta:
        db_table = 'snippets'
        verbose_name = _("Snippet")
        verbose_name_plural = _("Snippets")
        get_latest_by = 'date_added'
        ordering = ['date_added']

    def __str__(self):
        return '{0.title}'.format(self)

    def get_absolute_url(self):
        return reverse('app_snippets:snippet', kwargs={'slug': self.slug})

    def get_scope(self):
        pass
