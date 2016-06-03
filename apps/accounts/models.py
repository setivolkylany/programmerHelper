
import random
import shutil
import uuid

from django.utils import timezone
from importlib import import_module
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.conf import settings

from autoslug import AutoSlugField
from model_utils import Choices
from model_utils.managers import QueryManager

from apps.articles.models import Article
from apps.actions.models import Action
from apps.forum.models import ForumTopic
from apps.badges.managers import BadgeManager
from apps.sessions.models import ExpandedSession
from mylabour import utils
# from mylabour.fields_db import PhoneField

from .managers import AccountManager, AccountQuerySet


class AccountLevel(models.Model):
    """

    """

    CHOICES_LEVEL = Choices(
        ('platinum', _('Platinum')),
        ('golden', _('Gold')),
        ('silver', _('Silver')),
        ('diamond', _('Diamond')),
        ('ruby', _('Ruby')),
        ('sapphire', _('Sapphire')),
        ('malachite', _('Malachite')),
        ('amethyst', _('Amethyst')),
        ('emerald', _('Emerald')),
        ('agate', _('Agate')),
        ('turquoise', _('Turquoise')),
        ('amber', _('Amber')),
        ('opal', _('Opal')),
        ('regular', _('Regular')),
    )

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    name = models.CharField(_('Name'), max_length=50, choices=CHOICES_LEVEL, unique=True)
    slug = AutoSlugField(_('Slug'), populate_from='name', unique=True, always_update=True, allow_unicode=True, db_index=True)
    description = models.TextField(_('Description'))
    color = models.CharField(_('Color'), max_length=50)

    class Meta:
        db_table = 'account_levels'
        verbose_name = _('Level')
        verbose_name_plural = _('Levels')
        ordering = ['name']

    objects = models.Manager()

    def __str__(self):
        return '{0.name}'.format(self)

    def save(self, *args, **kwargs):
        super(AccountLevel, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('accounts:level', kwargs={'slug': self.slug})


class Account(AbstractBaseUser, PermissionsMixin):
    """
    Custom auth user model with additional fields and username fields as email
    """

    CHOICES_GENDER = Choices(
        ('vague', _('Vague')),
        ('man', _('Man')),
        ('woman', _('Woman')),
    )

    PATH_TO_ACCOUNT_DEFAULT_PICTURES = settings.STATIC_ROOT + '/accounts/images/avatar_pictures_default/'

    # account detail
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(
        _('Email'),
        unique=True,
        error_messages={
            'unique': _('Account with this email already exists.')
        }
    )
    username = models.CharField(_('Username'), max_length=200, help_text=_('Displayed name'))
    is_active = models.BooleanField(_('Is active'), default=True, help_text=_('Designated that this user is not disabled.'))
    profile_views = models.IntegerField(_('Profile views'), default=0, editable=False)
    date_joined = models.DateTimeField(_('Date joined'), auto_now_add=True)
    level = models.ForeignKey(
        'AccountLevel',
        verbose_name='Level',
        related_name='accounts',
        null=True,
        blank=True,
        on_delete=models.PROTECT,
    )
    picture = models.FilePathField(
        path=PATH_TO_ACCOUNT_DEFAULT_PICTURES,
        match='.*',
        recursive=True,
        verbose_name=_('Picture'),
        max_length=200,
        blank=True,
        allow_folders=False,
        allow_files=True,
    )
    signature = models.CharField(_('Signature'), max_length=50, default='')
    # presents in web
    presents_on_gmail = models.URLField(_('Presents on google services'), default='')
    presents_on_github = models.URLField(_('Presents on github'), default='')
    presents_on_stackoverflow = models.URLField(_('Presents on stackoverflow'), default='')
    personal_website = models.URLField(_('Personal website'), default='')
    # private fields
    gender = models.CharField(_('Gender'), max_length=50, choices=CHOICES_GENDER, default=CHOICES_GENDER.vague)
    date_birthday = models.DateField(_('Date birthday'))
    real_name = models.CharField(_('Real name'), max_length=200, default='')
    # phone = PhoneField(_('Phone'), default='')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'date_birthday']

    # managers
    objects = models.Manager()
    objects = AccountManager.from_queryset(AccountQuerySet)()
    badges_manager = BadgeManager()

    # simple managers
    actives = QueryManager(is_active=True)
    superusers = QueryManager(is_superuser=True)

    class Meta:
        db_table = 'account'
        verbose_name = _("Account")
        verbose_name_plural = _("Accounts")
        ordering = ['-last_login']  # not worked
        get_latest_by = 'date_joined'

    def __str__(self):
        return '{0.email}'.format(self)

    def save(self, *args, **kwargs):
        if not self.picture:
            files = shutil.os.listdir(self.PATH_TO_ACCOUNT_DEFAULT_PICTURES)
            if files:
                self.picture = self.PATH_TO_ACCOUNT_DEFAULT_PICTURES + random.choice(files)
        if self.level is None:
            default_level = AccountLevel.objects.get(name=AccountLevel.CHOICES_LEVEL.regular)
            self.level = default_level
        super(Account, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('accounts:detail', kwargs={'account_email': self.email})

    def get_full_name(self):
        return '{0.username} ({0.email})'.format(self)

    def get_short_name(self):
        return '{0.email}'.format(self)

    @property
    def is_staff(self):
        return self.is_superuser

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, label):
        return True

    def _as_queryset(self):
        return self.__class__.objects.filter(pk=self.pk)

    def last_seen(self):
        last_session_of_account = ExpandedSession.objects.filter(account_pk=self.pk).order_by('expire_date').last()
        if last_session_of_account:
            SessionStore = import_module(settings.SESSION_ENGINE).SessionStore
            session = SessionStore(session_key=last_session_of_account.session_key)
            last_seen = session['last_seen']
            return last_seen
        return None

    def have_certain_count_consecutive_days(self, count_consecutive_days):
        if count_consecutive_days > 0:
            if count_consecutive_days <= self.days_attendances.count():
                list_all_dates = self.days_attendances.only('day_attendance').values_list('day_attendance', flat=True)
                # getting differents between dates as timedelta objects
                differents_dates = utils.get_different_between_elements(sequence=list_all_dates, left_to_right=False)
                # converting timedelta objects in numbers
                differents_dates = tuple(timedelta.days for timedelta in differents_dates)
                # find the groups consecutive elements
                groups_concecutive_elements = utils.show_concecutive_certain_element(differents_dates, 1)
                # determinate max count consecutive elements
                max_count_concecutive_elements = max(len(group) for group in groups_concecutive_elements)
                # add 1 for учитывания первого дня
                max_count_concecutive_elements = max_count_concecutive_elements + 1 if max_count_concecutive_elements else 0
                if 0 < count_consecutive_days <= max_count_concecutive_elements:
                    return True
            return False
        raise ValueError('Count consecutive days must be 1 or more,')

    def actions_with_accounts(self):
        return self.actions.filter(flag=Action.CHOICES_FLAGS.profiling).all()

    def check_badge(self, badge_name):
        instance = self._as_queryset()
        return self.__class__.badges_manager.validate_badges(accounts=instance, badges_names=[badge_name])

    def has_badge(self, badge_name):
        return self.__class__.badges_manager.has_badge(account=self, badge_name=badge_name)

    def get_reputation(self):
        """Getting reputation 1of account based on his activity, actions, badges."""
        return sum([
            self.get_reputation_for_badges(),
            self.get_reputation_for_actions(),
        ])

    def get_reputation_for_badges(self):
        """Getting reputation of account for badges."""
        return self.badges.count() * 10

    def get_total_scope_for_answers(self):
        """Getting total scope for answers of account."""
        # getting instance as queryset
        queryset = self.__class__.objects.filter(email=self.email)
        # pass single queryset for execution once iteration in method of manager
        account_with_total_scope_for_answers = self.__class__.objects.accounts_with_total_scope_for_answers(queryset=queryset)
        # getting back instance after processing
        account_with_total_scope_for_answers = account_with_total_scope_for_answers.get()
        # return total_scope_for_answers of instance
        return account_with_total_scope_for_answers.total_scope_for_answers

    def get_total_scope_for_questions(self):
        """Getting total scope for questions of account."""
        # getting instance as queryset
        queryset = self.__class__.objects.filter(email=self.email)
        # pass single queryset for execution once iteration in method of manager
        account_with_total_scope_for_questions = self.__class__.objects.accounts_with_total_scope_for_questions(queryset=queryset)
        # getting back instance after processing
        account_with_total_scope_for_questions = account_with_total_scope_for_questions.get()
        # return total_scope_for_questions of instance
        return account_with_total_scope_for_questions.total_scope_for_questions

    def get_total_scope_for_solutions(self):
        """Getting total scope for solutions of account."""
        # getting instance as queryset
        queryset = self.__class__.objects.filter(email=self.email)
        # pass single queryset for execution once iteration in method of manager
        account_with_total_scope_for_solutions = self.__class__.objects.accounts_with_total_scope_for_solutions(queryset=queryset)
        # getting back instance after processing
        account_with_total_scope_for_solutions = account_with_total_scope_for_solutions.get()
        # return total_scope_for_solutions of instance
        return account_with_total_scope_for_solutions.total_scope_for_solutions

    def get_total_scope_for_snippets(self):
        """Getting total scope for snippets of account."""
        # getting instance as queryset
        queryset = self.__class__.objects.filter(email=self.email)
        # pass single queryset for execution once iteration in method of manager
        account_with_total_scope_for_snippets = self.__class__.objects.accounts_with_total_scope_for_snippets(queryset=queryset)
        # getting back instance after processing
        account_with_total_scope_for_snippets = account_with_total_scope_for_snippets.get()
        # return total_scope_for_snippets of instance
        return account_with_total_scope_for_snippets.total_scope_for_snippets

    def get_count_participate_in_polls(self):
        """Getting how many polls of account participated."""
        return self.votes_in_polls.count()

    def get_percent_filled_account_profile(self):
        """Getting percent filled profile of account."""
        return self.__class__.objects.get_filled_accounts_profiles()[self.pk]

    def get_total_rating_for_articles(self):
        """Getting total ratings of all articles of account."""
        evaluation_total_rating_for_articles_of_account = Article.objects.articles_with_rating().filter(author=self).aggregate(
            total_rating_for_articles=models.Sum('rating')
        )
        # return 0 if account not have articles
        total_rating_for_articles = evaluation_total_rating_for_articles_of_account['total_rating_for_articles'] or 0
        return total_rating_for_articles
        # 3.8
        # фотийодинцова@hotmail.com

    def get_count_popular_topics(self):
        """Getting count popular topics of account."""
        popular_topics_of_account = ForumTopic.objects.popular_topics().filter(author=self)
        return popular_topics_of_account.count()

    def get_count_testing_suits_in_which_account_involed(self):
        """In creating, how many testing suit involved account."""
        return self.testing_suits.count()

    def get_count_courses_in_which_account_involed(self):
        """In creating, how many testSuit involved account."""
        return self.courses.count()

    def get_reputation_for_actions(self):
        """
        Getting reputation of account for actions on website:
        scopes of published snippets, answers, questions and rating of articles,
        participate in polls.
        ---------------------------------------
            Evaluate reputation for actions
        ---------------------------------------
        Scope answers                   = *2
        Scope questions                 = *1
        Scope solutions                 = *3
        Rating articles                 = *4
        Scope snippets                  = *2
        Filled profile                  = *1
        Participate in poll             = *1
        Popular topic                   = *100
        Participate in creating tests   = *100
        Participate in creating courses = *200
        ---------------------------------------
        """
        reputation_for_snippets = (self.get_total_scope_for_snippets() or 0) * 2
        reputation_for_solutions = (self.get_total_scope_for_solutions() or 0) * 3
        reputation_for_questions = (self.get_total_scope_for_questions() or 0) * 1
        reputation_for_answers = (self.get_total_scope_for_answers() or 0) * 2
        reputation_for_polls = self.get_count_participate_in_polls() or 0
        reputation_for_filled_account_profile = self.get_percent_filled_account_profile() or 0
        reputation_for_polls = (self.get_total_rating_for_articles() or 0) * 4
        reputation_for_polls = (self.get_count_popular_topics() or 0) * 100
        reputation_for_test_suits = (self.get_count_testing_suits_in_which_account_involed() or 0) * 100
        reputation_for_courses = (self.get_count_courses_in_which_account_involed() or 0) * 200
        return sum([
            reputation_for_snippets,
            reputation_for_solutions,
            reputation_for_questions,
            reputation_for_answers,
            reputation_for_polls,
            reputation_for_filled_account_profile,
            reputation_for_polls,
            reputation_for_polls,
            reputation_for_test_suits,
            reputation_for_courses,
        ])