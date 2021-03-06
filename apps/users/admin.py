
import collections
import logging

from django.db import models
from django.db.models.fields import BLANK_CHOICE_DASH
from django.core.urlresolvers import reverse
from django.conf.urls import url
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from apps.admin.site import DefaultSiteAdmin
from apps.admin.admin import ModelAdmin, StackedInline, TabularInline
from apps.admin.app import AppAdmin
from apps.admin.utils import register_model, register_app
from apps.polls.listfilters import IsActiveVoterListFilter

from .actions import (
    make_users_as_non_superuser,
    make_users_as_superuser,
    make_users_as_non_active,
    make_users_as_active,
)
from .constants import LEVELS
from .forms import UserChangeForm, UserCreateAdminModelForm, LevelAdminModelForm, ProfileAdminModelForm
from .models import User, Level, Profile
from .listfilters import ListFilterLastLogin
from .apps import UsersConfig


logger = logging.getLogger('django.development')


@register_app
class UserAppAdmin(AppAdmin):

    app_config_class = UsersConfig
    app_icon = 'users'


class ProfileInline(StackedInline):

    template = 'users/admin/edit_inline/stacked_OneToOne.html'
    model = Profile
    fields = (
        'views',
        'about',
        'signature',
        'on_gmail',
        'on_github',
        'on_stackoverflow',
        'website',
        'gender',
        'job',
        # 'location',
        'latitude',
        'longitude',
        'phone',
        'date_birthday',
        'real_name',
    )
    readonly_fields = (
        'views',
        'about',
        'signature',
        'on_gmail',
        'on_github',
        'on_stackoverflow',
        'website',
        'gender',
        'job',
        # 'location',
        'latitude',
        'longitude',
        'phone',
        'date_birthday',
        'real_name',
    )
    show_change_link = True
    verbose_name_plural = ''

    suit_classes = 'suit-tab suit-tab-profile'


# class UserAdminModel(BaseUserAdmin):
@register_model(User)
class UserAdminModel(ModelAdmin):
    """
    Admin configuration for model User
    """

    max_count_display_queryset = 3
    form = UserChangeForm
    add_form = UserCreateAdminModelForm
    actions = (
        make_users_as_non_superuser,
        make_users_as_superuser,
        make_users_as_non_active,
        make_users_as_active,
    )

    list_display = [
        ('users_main_info', {
            'title': _('Users (main information)'),
            'fields': (
                'alias',
                'username',
                'email',
                'is_active',
                'is_superuser',
                'date_joined',
            ),
        }),
        ('users_extra_info', {
            'title': _('Users (extra information)'),
            'fields': (
                'alias',
                'username',
                'email',
                'level',
                'reputation',
                'last_login',
            ),
        }),
        ('users_visits', {
            'title': _('Users and visits'),
            'fields': (
                'alias',
                'get_last_seen',
                'get_count_days_attendances',
            ),
            'filters': [],
            'ordering': [],
        }),
        ('users_polls', {
            'title': _('Users and polls'),
            'fields': (
                '__str__',
                'get_count_votes',
                'is_active_voter',
                'get_date_latest_vote',
            ),
        }),
        ('users_questions', {
            'title': _('Users and questions'),
            'fields': (
                '__str__',
                'get_favorite_tags_on_questions',
                'get_count_questions',
                'get_total_rating_on_questions',
                'get_total_count_answers_on_questions',
                'get_count_opinions_on_questions',
                'get_count_good_opinions_on_questions',
                'get_count_bad_opinions_on_questions',
                'get_date_latest_question',
            ),
        }),
        ('users_answers', {
            'title': _('Users and answers'),
            'fields': (
                '__str__',
                'get_favorite_tags_on_answers',
                'get_count_answers',
                'get_total_rating_on_answers',
                'get_count_opinions_on_answers',
                'get_count_good_opinions_on_answers',
                'get_count_bad_opinions_on_answers',
                'get_count_comments_on_its_answers',
                'get_date_latest_answer',
            ),
        }),
        ('users_articles', {
            'title': _('Users and articles'),
            'fields': (
                '__str__',
                'get_count_articles',
                'get_total_rating_on_articles',
                'get_favorite_tags_on_articles',
                'get_count_marks_on_articles',
                'get_count_comments_on_its_articles',
                'get_date_latest_article',
            ),
        }),
        ('users_solutions', {
            'title': _('Users and solutions'),
            'fields': (
                '__str__',
                'get_favorite_tags_on_solutions',
                'get_count_solutions',
                'get_total_rating_on_solutions',
                'get_count_opinions_on_solutions',
                'get_count_good_opinions_on_solutions',
                'get_count_bad_opinions_on_solutions',
                'get_count_comments_on_its_solutions',
                'get_date_latest_solution',
            ),
        }),

        ('users_snippets', {
            'title': _('Users and snippets'),
            'fields': (
                '__str__',
                'get_favorite_tags_on_snippets',
                'get_count_snippets',
                'get_total_rating_on_snippets',
                'get_count_opinions_on_snippets',
                'get_count_good_opinions_on_snippets',
                'get_count_bad_opinions_on_snippets',
                'get_count_comments_on_its_snippets',
                'get_date_latest_snippet',
            ),
        }),

        ('users_comments', {
            'title': _('Users and comments'),
            'fields': (
                '__str__',
                'get_count_comments_on_articles_other_users',
                'get_count_comments_on_solutions_other_users',
                'get_count_comments_on_snippets_other_users',
                'get_count_comments_on_answers_other_users',
                'get_count_comments_on_utilities',
                'get_total_count_comments',
                'get_date_latest_comment',
            ),
        }),

        ('users_library', {
            'title': _('Users and library'),
            'fields': (
                '__str__',
                'get_count_replies',
                'get_book_with_latest_reply_and_admin_url',
                'get_date_latest_reply',
            ),
        }),

        ('users_opinions', {
            'title': _('Users and opinions'),
            'fields': (
                '__str__',
                'get_count_opinions_on_solutions_other_users',
                'get_count_opinions_on_snippets_other_users',
                'get_count_opinions_on_questions_other_users',
                'get_count_opinions_on_answers_other_users',
                'get_count_opinions_on_utilities',
                'get_total_count_opinions',
                'get_date_latest_opinion',
            ),
        }),

        ('users_marks', {
            'title': _('Users and marks'),
            'fields': (
                '__str__',
                'get_total_count_marks',
                'get_article_with_latest_mark_and_admin_url',
                'get_date_latest_mark',
            ),
        }),

        ('users_badges', {
            'title': _('Users and badges'),
            'fields': (
                '__str__',
                'get_count_bronze_badges',
                'get_count_silver_badges',
                'get_count_gold_badges',
                'get_count_earned_badges',
                'get_latest_badge',
                'get_date_getting_latest_badge',
            ),
        }),

        ('users_notifications', {
            'title': _('Users and notifications'),
            'fields': (
                '__str__',
                'get_count_unread_notifications',
                'get_count_read_notifications',
                'get_count_deleted_notifications',
                'get_total_count_notifications',
            ),
        }),

        ('users_forums', {
            'title': _('Users and forums'),
            'fields': (
                '__str__',
                'get_count_topics',
                'get_count_posts',
                'get_count_popular_topics',
                'get_date_latest_activity_on_forums',
            ),
        }),

        ('users_tags', {
            'title': _('Users and tags '),
            'fields': (
                '__str__',
                'get_favorite_tags',
                'get_count_used_unique_tags',
                'get_total_count_used_tags',
            ),
        }),

    ]

    list_display_links = ('alias', )
    list_display_styles = (
        (
            ('__all__', ), {
                'align': 'center',
            }
        ),
        (
            ('date_joined', 'last_login'), {
                'align': 'right',
            }
        )
    )

    list_filter = [
        # ('level', admin.RelatedOnlyFieldListFilter),
        # ('is_active', admin.BooleanFieldListFilter),
        # ('is_superuser', admin.BooleanFieldListFilter),
        # ListFilterLastLogin,
        # ('date_joined', admin.DateFieldListFilter),
    ]
    ordering = ('date_joined', )
    list_per_page = 15
    search_fields = ('alias', 'email', 'username')
    date_hierarchy = 'date_joined'

    filter_horizontal = ['groups']
    filter_vertical = ['user_permissions']
    add_fieldsets = (
        (
            None, {
                'fields': (
                    'email',
                    'username',
                    'alias',
                    'password1',
                    'password2',
                )
            }
        ),
    )
    readonly_fields = (
        'display_avatar',
        'last_login',
        # 'reputation',
        'level',
        'last_seen',
        'date_joined',
        'get_count_comments',
        'get_count_opinions',
        'get_count_likes',
        'get_count_marks',
        'get_count_questions',
        'get_count_snippets',
        'get_count_articles',
        'get_count_answers',
        'get_count_solutions',
        'get_count_posts',
        'get_count_topics',
        'get_count_test_suits',
        'get_count_passages',
        'get_count_votes',
        # 'display_diary_details',
    )

    def get_queryset(self, request, list_display_name=None):

        if list_display_name is None or list_display_name in ['users_main_info', 'users_extra_info']:

            qs = super(UserAdminModel, self).get_queryset(request)

        elif list_display_name == 'users_visits':

            qs = self.model.visits_manager.users_with_count_attendances()

        elif list_display_name == 'users_polls':

            qs = self.model.polls_manager\
                .users_with_count_votes_and_date_latest_voting_and_active_voters_status()

        elif list_display_name == 'users_questions':

            qs = self.model.questions_manager\
                .users_with_count_questions_and_date_latest_question_and_users_with_rating_by_questions()

        elif list_display_name == 'users_answers':

            qs = self.model.answers_manager\
                .users_with_count_answers_and_date_latest_answer_and_count_good_bad_total_opinions_on_answers()

        elif list_display_name == 'users_articles':

            qs = self.model.articles_manager\
                .users_with_count_articles_comments_marks_and_rating_and_date_latest_articles()

        elif list_display_name == 'users_solutions':

            qs = self.model.solutions_manager\
                .users_with_count_comments_solutions_bad_good_and_total_opinions_and_rating_and_date_latest_solutions()

        elif list_display_name == 'users_snippets':

            qs = self.model.snippets_manager\
                .users_with_count_comments_bad_good_and_total_opinions_and_rating_and_date_latest_snippets()

        elif list_display_name == 'users_comments':

            qs = self.model.comments_manager\
                .users_with_count_comments_on_its_related_objects_and_total_and_date_latest_comment()

        elif list_display_name == 'users_library':

            qs = self.model.replies_manager\
                .users_with_count_replies_and_date_latest_reply()

        elif list_display_name == 'users_opinions':

            qs = self.model.opinions_manager\
                .users_with_count_opinions_on_related_objects_and_total_and_date_latest_opinion()

        elif list_display_name == 'users_marks':

            qs = self.model.marks_manager.users_with_count_marks_and_latest_mark()

        elif list_display_name == 'users_badges':

            qs = self.model.badges_manager\
                .users_with_count_gold_silver_bronze_and_total_badges_and_date_getting_latest_badge()

        elif list_display_name == 'users_notifications':

            qs = self.model.notifications_manager\
                .users_with_count_deleted_read_unread_and_total_notifications()

        elif list_display_name == 'users_forums':

            qs = self.model.forums_manager\
                .users_with_count_posts_topic_popular_topic_and_date_latest_activity_on_forums()

        elif list_display_name == 'users_tags':

            qs = self.model.tags_manager\
                .users_with_count_used_unique_tags_and_total_count_used_tags()

        return qs

    def get_fieldsets(self, request, obj=None):

        if obj is None:
            self.suit_form_tabs = ()
            self.suit_form_includes = ()
            return self.add_fieldsets

        else:

            self.suit_form_tabs = (
                ('general', _('General')),
                ('permissions', _('Permissions')),
                ('groups', _('Groups')),
                ('tags', _('Tags')),
                ('badges', _('Badges')),
                ('activity', _('Activity')),
                ('notifications', _('Notifications')),
                ('summary', _('Summary')),
            )

            self.suit_form_includes = (
                ('users/admin/user_admin_tab_tags.html', 'top', 'tags'),
            )

            return (
                (
                    None, {
                        'classes': ('suit-tab suit-tab-general', ),
                        'fields': (
                            'alias',
                            'email',
                            'username',
                            'password',
                            'is_active',
                            'is_superuser',
                            'display_avatar',
                        )
                    },
                ),
                (
                    None, {
                        'classes': ('suit-tab suit-tab-permissions', ),
                        'fields': (
                            'user_permissions',
                        )
                    }
                ),
                (
                    None, {
                        'classes': ('suit-tab suit-tab-groups', ),
                        'fields': (
                            'groups',
                        )
                    }
                ),
                (
                    None, {
                        'classes': ('suit-tab suit-tab-summary', ),
                        'fields': (
                            'level',
                            # 'reputation',
                            'last_seen',
                            'last_login',
                            'date_joined',
                            # 'display_diary_details',
                            'get_count_comments',
                            'get_count_opinions',
                            'get_count_likes',
                            'get_count_marks',
                            'get_count_questions',
                            'get_count_snippets',
                            'get_count_articles',
                            'get_count_answers',
                            'get_count_solutions',
                            'get_count_posts',
                            'get_count_topics',
                            'get_count_test_suits',
                            'get_count_passages',
                            'get_count_votes',
                        )
                    }
                ),
            )

    def get_urls(self):

        urls = super(UserAdminModel, self).get_urls()

        additional_urls = [
        ]

        # additional urls must be before standartic urls
        urls = additional_urls + urls

        return urls

    def change_view(self, request, object_id, form_url='', extra_context=None):

        if extra_context is None:
            extra_context = {}

        statistics_usage_tags = self.model.objects.get(pk=object_id).get_statistics_usage_tags(20)

        extra_context['statistics_usage_tags'] = statistics_usage_tags

        # for reject unneccessary calculation use straight access instead user.get_top_tag()
        extra_context['user_top_tag'] = None if statistics_usage_tags is not None else statistics_usage_tags[0][0]

        return super(UserAdminModel, self).change_view(request, object_id, form_url, extra_context)

    def changelist_view(self, request, extra_context=None):

        # temproraly make a request.GET as a mutable object
        request.GET._mutable = True

        # get a custom value from a URL, if presents.
        # and keep this value on a instance of this class
        try:
            self.display_users = request.GET.pop('display_users')[0]
        except KeyError:
            self.display_users = None

        # restore the request.GET as a unmutable object
        request.GET._mutable = False

        if request.path == reverse('admin:users_user_changelist'):
            self.list_display = [
                'email',
                'username',
                'level',
                'is_active',
                'is_superuser',
                'last_login',
                'date_joined',
            ]
            self.list_filter = [
                # ('level', LevelRelatedOnlyFieldListFilter),
                ('is_active', admin.BooleanFieldListFilter),
                ('is_superuser', admin.BooleanFieldListFilter),
                ListFilterLastLogin,
                ('date_joined', admin.DateFieldListFilter),
            ]
            self.ordering = ['date_joined']

        response = super(UserAdminModel, self).changelist_view(request, extra_context)
        return response

    def get_inline_instances(self, request, obj=None):

        if obj is not None:
            # inlines = inlines
            return [inline(self.model, self.admin_site) for inline in inlines]
        return []

    def display_diary_details(self, obj):

        has_diary = obj.has_diary()

        msg = _('User has not a diary')
        link_url = reverse('admin:diaries_diary_add')
        link_text = _('Create now')

        return format_html(
            '<span>{}</span><form action="{}"><button type="submit">{}</button></form>', msg, link_url, link_text)

        if has_diary is True:
            msg = _('User has a diary')
            link_url = '2'
            link_text = _('Change it')

        return format_html('<span>{}</span><a href="{}">{}</a>', msg, link_url, link_text)


@register_model(Profile)
class ProfileAdminModel(ModelAdmin):

    list_display = (
        'user',
        'gender',
        'views',
        'get_percentage_filling',
        'updated',
    )

    list_display_styles = (
        (
            ('updated', ), {
                'align': 'right',
            }
        ),
        (
            ('user', ), {
                'align': 'left',
            }
        ),
        (
            ('get_percentage_filling', 'views', 'gender'), {
                'align': 'center',
            }
        ),
    )

    colored_rows_by = 'determinate_color_rows'

    readonly_fields = (
        'get_user__display_avatar',
        'get_user__get_full_name',
        'display_location',
        'longitude',
        'views',
        'updated',
        'latitude',
    )
    search_fields = ('user', )
    date_hierarchy = 'updated'
    list_filter = (
        'gender',
        'updated',
    )

    form = ProfileAdminModelForm

    def get_fieldsets(self, request, obj=None):

        fieldsets = (
            (
                _('Public information'), {
                    'fields': (
                        'get_user__display_avatar',
                        'about',
                        'crafts',
                        'views',
                        'signature',
                        'on_gmail',
                        'on_github',
                        'on_stackoverflow',
                        'website',
                    ),
                }
            ),
            (
                _('Private information'), {
                    'fields': (
                        'display_location',
                        'gender',
                        'job',
                        'date_birthday',
                        'real_name',
                        'phone',
                        'updated',
                    ),
                }
            ),
            (
                _('Preferences'), {
                    'fields': (
                        'show_email',
                        'show_location',
                    ),
                }
            ),
        )

        return fieldsets

    def determinate_color_rows(self, obj):
        percentage_filling = obj.get_percentage_filling()
        percentage_filling = percentage_filling.strip('%')
        percentage_filling = float(percentage_filling)

        row_color = None
        if percentage_filling >= 90:
            row_color = 'success'
        elif percentage_filling <= 25:
            row_color = 'danger'

        return row_color

    def get_user__display_avatar(self, obj):
        return obj.user.display_avatar()
    get_user__display_avatar.short_description = _('Avatar')

    def get_user__get_full_name(self, obj):
        return obj.user.get_full_name()
    get_user__get_full_name.short_description = _('User')


class UserInline(TabularInline):

    model = User
    fields = ('get_full_name', 'reputation', 'date_joined')
    readonly_fields = ('get_full_name', 'reputation', 'date_joined')
    readonly_fields_tabular_align = {
        'get_full_name': 'left',
        'reputation': 'center',
        'date_joined': 'right',
    }
    max_num = 0
    extra = 0
    can_delete = False


@register_model(Level)
class LevelAdminModel(ModelAdmin):
    '''
    Admin View for Level
    '''

    form = LevelAdminModelForm
    list_display = (
        'name',
        'get_count_users',
        'display_color',
        'description',
    )
    list_display_styles = (
        (
            ('__str__', ), {
                'align': 'left',
            }
        ),
        (
            ('get_count_users', ), {
                'align': 'center',
            }
        ),
        (
            ('name', ), {
                'align': 'center',
            },
        ),
    )
    search_fields = ('name', 'description')
    fieldsets = (
        (
            Level._meta.verbose_name, {
                'fields': (
                    'name',
                    'color',
                    'description',
                ),
            },
        ),
    )

    def get_queryset(self, request):

        qs = super().get_queryset(request)
        qs = qs.levels_with_count_users()
        return qs

    def formfield_for_choice_field(self, db_field, request, **kwargs):

        if db_field.name == "name":
            qs = self.get_queryset(request)
            pk = request.resolver_match.kwargs.get('pk')
            if pk is not None:
                qs = qs.exclude(pk=pk)
            used_level_names = qs.values_list('name', flat=True)
            unused_level_names = [
                choice for choice in db_field.model.CHOICES_LEVEL
                if choice[0] not in used_level_names
            ]

            unused_level_names.insert(0, BLANK_CHOICE_DASH[0])

            kwargs['choices'] = unused_level_names

        return super().formfield_for_choice_field(db_field, request, **kwargs)

    def get_inline_instances(self, request, obj=None):

        if obj is None:
            return []

        inlines = [UserInline]
        return [inline(self.model, self.site_admin) for inline in inlines]

    def display_color(self, obj):
        """ """

        return format_html(
            '<span style="background-color: {};">&nbsp;&nbsp;&nbsp;&nbsp;</span>&nbsp;{}',
            obj.color, obj.color,
        )
    display_color.short_description = Level._meta.get_field('color').verbose_name
    display_color.admin_order_field = 'color'
