
from django.contrib.contenttypes.admin import GenericStackedInline, GenericTabularInline
from django.contrib import admin

from .models import CommentGeneric, OpinionGeneric, LikeGeneric, ScopeGeneric
from .forms import ScopeGenericInlineFormSet


class CommentGenericAdmin(admin.ModelAdmin):
    '''
    Admin View for CommentGeneric
    '''

    list_display = ('content_object', 'content_type', 'author', 'is_new', 'date_modified', 'date_added')
    list_filter = (
        ('content_type', admin.RelatedOnlyFieldListFilter),
        ('author', admin.RelatedOnlyFieldListFilter),
        'date_modified',
        'date_added',
    )
    date_hierarchy = 'date_modified'
    search_fields = ('content_object',)
    fieldsets = [
        [
            CommentGeneric._meta.verbose_name, {
                'fields': ['content_type', 'object_id', 'author', 'text_comment'],
            }
        ]
    ]
    readonly_fields = ['author', 'content_type', 'text_comment', 'object_id']


class OpinionGenericAdmin(admin.ModelAdmin):
    '''
    Admin View for OpinionGeneric
    '''

    list_display = (
        'content_object',
        'content_type',
        'user',
        'is_useful',
        'is_favorite',
        'is_new',
        'date_modified',
    )
    list_filter = (
        ('content_type', admin.RelatedOnlyFieldListFilter),
        ('user', admin.RelatedOnlyFieldListFilter),
        'is_useful',
        'is_favorite',
        'date_modified',
    )
    date_hierarchy = 'date_modified'
    search_fields = ('content_object',)
    fieldsets = [
        [
            OpinionGeneric._meta.verbose_name, {
                'fields': ['content_type', 'object_id', 'user', 'is_useful', 'is_favorite'],
            }
        ]
    ]
    readonly_fields = ['content_type', 'object_id', 'user', 'is_useful', 'is_favorite']


class LikeGenericAdmin(admin.ModelAdmin):
    '''
    Admin View for LikeGeneric
    '''

    list_display = (
        'content_object',
        'content_type',
        'user',
        'liked_it',
        'is_new',
        'date_modified',
    )
    list_filter = (
        ('content_type', admin.RelatedOnlyFieldListFilter),
        ('user', admin.RelatedOnlyFieldListFilter),
        'liked_it',
        'date_modified',
    )
    date_hierarchy = 'date_modified'
    search_fields = ('content_object',)
    fieldsets = [
        [
            LikeGeneric._meta.verbose_name, {
                'fields': ['content_type', 'object_id', 'user', 'liked_it'],
            }
        ]
    ]
    readonly_fields = ['content_type', 'object_id', 'user', 'liked_it']


class ScopeGenericAdmin(admin.ModelAdmin):
    '''
    Admin View for LikeGeneric
    '''

    list_display = (
        'content_object',
        'content_type',
        'user',
        'scope',
        'is_new',
        'date_modified',
        'object_id',
    )
    list_filter = (
        ('content_type', admin.RelatedOnlyFieldListFilter),
        ('user', admin.RelatedOnlyFieldListFilter),
        'scope',
        'date_modified',
    )
    date_hierarchy = 'date_modified'
    search_fields = ('content_object',)
    fieldsets = [
        [
            ScopeGeneric._meta.verbose_name, {
                'fields': ['content_type', 'object_id', 'user', 'scope'],
            }
        ]
    ]
    readonly_fields = ['content_type', 'object_id', 'user', 'scope']


class OpinionGenericInline(GenericTabularInline):
    model = OpinionGeneric
    extra = 0
    fields = ['user', 'is_useful', 'is_favorite']


class CommentGenericInline(GenericStackedInline):
    model = CommentGeneric
    extra = 0
    fields = ['author', 'text_comment']


class LikeGenericInline(GenericTabularInline):
    model = LikeGeneric
    extra = 0
    fields = ['user', 'liked_it']


class ScopeGenericInline(GenericTabularInline):
    model = ScopeGeneric
    extra = 0
    fields = ['user', 'scope']
    formset = ScopeGenericInlineFormSet
