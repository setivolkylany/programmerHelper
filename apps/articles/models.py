
from django.db.models import Avg
from django.contrib.contenttypes.fields import GenericRelation
from django.core.urlresolvers import reverse
from django.core.validators import MinLengthValidator, RegexValidator, MinValueValidator, MaxValueValidator
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.conf import settings

from model_utils.fields import StatusField, MonitorField
from model_utils import Choices
from autoslug import AutoSlugField

from mylabour.models import TimeStampedModel
from apps.comments.models import Comment
from apps.scopes.models import Scope
from apps.tags.models import Tag
from apps.web_links.models import WebLink
from mylabour.fields_db import ConfiguredAutoSlugField

from .managers import ArticleManager, ArticleQuerySet


class Article(TimeStampedModel):
    """
    Model for article
    """

    MIN_COUNT_SUBSECTIONS = 1
    MAX_COUNT_SUBSECTIONS = 5

    STATUS_ARTICLE = Choices(
        ('draft', _('Draft')),
        ('published', _('Published')),
    )

    title = models.CharField(
        _('Title'), max_length=200, validators=[MinLengthValidator(settings.MIN_LENGTH_FOR_NAME_OR_TITLE_OBJECT)]
    )
    slug = ConfiguredAutoSlugField(_('Slug'), populate_from='title', unique_with=['account'])
    quotation = models.CharField(_('Quotation'), max_length=200)
    picture = models.URLField(_('Picture'), max_length=1000)
    header = models.TextField(_('Header'))
    conclusion = models.TextField(_('Conclusion'))
    status = StatusField(verbose_name=_('Status'), choices_name='STATUS_ARTICLE', default=STATUS_ARTICLE.draft)
    status_changed = MonitorField(monitor='status', verbose_name=_('Status changed'))
    account = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('Author'),
        related_name='articles',
        limit_choices_to={'is_active': True},
        on_delete=models.CASCADE,
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='articles',
        verbose_name=_('Tags'),
    )
    links = models.ManyToManyField(
        WebLink,
        related_name='articles',
        verbose_name=_('Links'),
        help_text=_('Useful links'),
    )
    comments = GenericRelation(Comment)
    scopes = GenericRelation(Scope)

    # managers
    objects = models.Manager()
    objects = ArticleManager.from_queryset(ArticleQuerySet)()

    class Meta:
        db_table = 'articles'
        verbose_name = _("Article")
        verbose_name_plural = _("Articles")
        get_latest_by = 'date_added'
        ordering = ['date_added']
        unique_together = ['account', 'title']

    def __str__(self):
        return '{0.title}'.format(self)

    def save(self, *args, **kwargs):
        # self.slug =
        super(Article, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('articles:article', kwargs={'slug': self.slug})

    def get_rating(self):
        rating = self.scopes.aggregate(rating=Avg('scope'))['rating']
        if rating is not None:
            return float('{0:.3}'.format(rating))
        return None
    get_rating.admin_order_field = 'rating'  # annotation in admin.py
    get_rating.short_description = _('Rating')


class ArticleSubsection(TimeStampedModel):

    article = models.ForeignKey(
        'Article',
        related_name='subsections',
        on_delete=models.CASCADE,
        verbose_name=_('Article'),
    )
    title = models.CharField(
        _('Title'), max_length=200, validators=[MinLengthValidator(settings.MIN_LENGTH_FOR_NAME_OR_TITLE_OBJECT)]
    )
    slug = AutoSlugField(
        _('Slug'), populate_from='title', unique_with=['article'], always_update=True, allow_unicode=True, db_index=True
    )
    content = models.TextField(_('Content'))

    class Meta:
        db_table = 'articles_subsections'
        verbose_name = _("Subsection")
        verbose_name_plural = _("Subsections")
        ordering = ['article', 'date_modified']
        unique_together = ['article', 'title']

    def __str__(self):
        return '{0.title}'.format(self)