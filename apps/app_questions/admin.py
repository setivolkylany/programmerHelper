
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin
from django.db.models import Count

from apps.app_generic_models.admin import OpinionGenericInline, CommentGenericInline, LikeGenericInline

from .forms import QuestionForm
from .models import Answer


class AnswerInline(admin.StackedInline):
    '''
    Stacked Inline View for Answer
    '''

    model = Answer
    extra = 0
    fk_name = 'question'
    fields = ['author', 'is_acceptabled', 'text_answer']


class QuestionAdmin(admin.ModelAdmin):
    '''
    Admin View for Question
    '''

    list_display = (
        'title',
        'author',
        'status',
        'get_count_answers',
        'get_scope',
        'get_count_opinions',
        'get_count_tags',
        'is_dublicated',
        'is_new',
        'last_activity',
        'date_modified',
        'date_added')
    list_filter = (
        ('author', admin.RelatedFieldListFilter),
        'status',
        'date_modified',
        'date_added',
        'is_dublicated',
    )
    inlines = [
        OpinionGenericInline,
        AnswerInline,
    ]
    fieldsets = [
        (_('Question'), {
            'fields': ['title', 'author', 'status', 'text_question', 'is_dublicated', 'tags'],
        }),
    ]
    filter_horizontal = ['tags']
    form = QuestionForm
    search_fields = ['title']

    def get_queryset(self, request):
        qs = super(QuestionAdmin, self).get_queryset(request)
        qs = qs.annotate(
            count_answers=Count('answers', distinct=True),
            count_tags=Count('tags', distinct=True),
            count_opinions=Count('opinions', distinct=True),
        )
        return qs

    def get_count_answers(self, obj):
        return obj.count_answers
    get_count_answers.admin_order_field = 'count_answers'
    get_count_answers.short_description = _('Count answers')

    def get_count_tags(self, obj):
        return obj.count_tags
    get_count_tags.admin_order_field = 'count_tags'
    get_count_tags.short_description = _('Count tags')

    def get_count_opinions(self, obj):
        return obj.count_opinions
    get_count_opinions.admin_order_field = 'count_opinions'
    get_count_opinions.short_description = _('Count opinions')


class AnswerAdmin(admin.ModelAdmin):
    '''
        Admin View for Answer
    '''

    list_display = (
        'question',
        'author',
        'is_acceptabled',
        'get_count_comments',
        'get_count_likes',
        'get_scope',
        'is_new',
        'date_modified',
        'date_added',
    )
    list_filter = (
        ('author', admin.RelatedFieldListFilter),
        ('question', admin.RelatedFieldListFilter),
        'is_acceptabled',
        'date_modified',
        'date_added',
    )
    date_hierarchy = 'date_added'
    inlines = [
        LikeGenericInline,
        CommentGenericInline,
    ]
    fields = ['question', 'author', 'text_answer', 'is_acceptabled']

    def get_queryset(self, request):
        qs = super(AnswerAdmin, self).get_queryset(request)
        qs = qs.annotate(
            count_likes=Count('likes', distinct=True),
            count_comments=Count('comments', distinct=True),
        )
        return qs

    def get_count_likes(self, obj):
        return obj.count_likes
    get_count_likes.admin_order_field = 'count_likes'
    get_count_likes.short_description = _('Count voted opinions')

    def get_count_comments(self, obj):
        return obj.count_comments
    get_count_comments.admin_order_field = 'count_comments'
    get_count_comments.short_description = _('Count comments')
