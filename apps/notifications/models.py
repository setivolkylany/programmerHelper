
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.conf import settings

from utils.django.models import UUIDable

from .constants import Actions
from .managers import (
    NotificationManager,
    NotificationBadgeManager,
    NotificationActivityManager,
    NotificationReputationManager,
)


class Notification(UUIDable):
    """ """

    ANONIMUOS_DISPLAY_TEXT = _('Anonimuos user')

    SUCCESS = 'success'
    INFO = 'info'
    ERROR = 'error'
    WARNING = 'warning'

    CHOICES_LEVEL = (
        (SUCCESS, _('Success')),
        (INFO, _('Info')),
        (ERROR, _('Error')),
        (WARNING, _('Warning')),
    )

    level = models.CharField(_('level'), default=SUCCESS, choices=CHOICES_LEVEL, max_length=10)
    action = models.CharField(_('action'), max_length=200)

    is_read = models.BooleanField(_('is read?'), default=False, db_index=True)
    is_deleted = models.BooleanField(_('is deleted?'), default=False)
    is_public = models.BooleanField(_('is public?'), default=True)
    is_emailed = models.BooleanField(_('is emailed?'), default=True)

    created = models.DateTimeField(_('created'), auto_now_add=True)

    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL, models.CASCADE,
        verbose_name=_('recipient'), related_name='notifications',
    )

    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL, models.SET_NULL, verbose_name=_('actor'),
        related_name='+', null=True, blank=True, db_index=True,
    )
    actor_display_text = models.CharField(_('actor_display_text'), max_length=100, blank=True)

    target_content_type = models.ForeignKey(
        ContentType, models.SET_NULL, null=True,
        blank=True, related_name='notifications_targets',
    )
    target_object_id = models.CharField(max_length=200, null=True, blank=True)
    target = GenericForeignKey(ct_field='target_content_type', fk_field='target_object_id')
    target_display_text = models.CharField(_('target'), max_length=200, null=True, blank=True)

    action_target_content_type = models.ForeignKey(
        ContentType, models.SET_NULL, blank=True,
        null=True, related_name='notifications_action_targets',
    )
    action_target_object_id = models.CharField(max_length=200, null=True, blank=True)
    action_target = GenericForeignKey(ct_field='action_target_content_type', fk_field='action_target_object_id')

    # managers
    objects = models.Manager()
    notifications = NotificationManager()
    notifications_badges = NotificationBadgeManager()
    notifications_activity = NotificationActivityManager()
    notifications_reputation = NotificationReputationManager()

    class Meta:
        verbose_name = _('notification')
        verbose_name_plural = _('notifications')
        get_latest_by = 'created'
        ordering = ('-created', )

    def __str__(self):

        if self.created is None:
            recipient = self.recipient if hasattr(self, 'recipient') else 'unknown user'
            return 'for {}'.format(recipient)

        action_display_pattern = self.get_action_display_pattern()
        target = self.target_display_text if self.target is None else self.target

        actor_type = 'ERRRROR' if self.actor is None else self.actor._meta.verbose_name
        action_display_pattern = action_display_pattern % dict(
            actor=self.get_actor_display_text(),
            actor_type=actor_type,
            target=target,
            target_type=self.target_type_verbose_name,
            action_target_type=self.action_target_type_verbose_name,
            reputation_deviation=self.get_reputation_deviation(),
            recipient=self.recipient,
        )
        return 'for {}: {}'.format(self.recipient, action_display_pattern)

    def save(self, *args, **kwargs):

        target = kwargs.pop('target', None)
        if target is not None:
            self.target_display_text = str(target)

        actor = kwargs.pop('actor', None)
        if actor is not None:
            self.actor_display_text = actor.get_full_name()

        if self.is_deleted is True:
            self.is_read = True

        self.full_clean()
        super(Notification, self).save(*args, **kwargs)

    def mark_as_read(self):

        if self.is_read is False:
            self.is_read = True
            self.full_clean()
            self.save()

    def mark_as_unread(self):

        if self.is_read is True:
            self.is_read = False
            self.full_clean()
            self.save()

    def mark_as_deleted(self):

        if self.is_deleted is False:
            self.is_deleted = True
            self.full_clean()
            self.save()

    def mark_as_undeleted(self):

        if self.is_deleted is True:
            self.is_deleted = False
            self.full_clean()
            self.save()

    def get_target_info(self):

        if self.target is None:
            target_content_type_name = self.target_content_type.model_class()._meta.verbose_name.lower()
            target_display_text = self.target_display_text
        else:
            target_content_type_name = self.target._meta.verbose_name.lower()
            target_display_text = str(self.target)

        return target_content_type_name, target_display_text

    def get_actor_display_text(self):

        if self.actor is None:
            return self.actor_display_text
        return self.actor.get_full_name()

    @property
    def target_type_verbose_name(self):

        if self.target_content_type is None:
            return 'self.actor_verbose_name'

        target_model = self.target_content_type.model_class()
        return target_model._meta.verbose_name

    @property
    def action_target_type_verbose_name(self):

        if self.action_target_content_type is not None:

            action_target_model = self.action_target_content_type.model_class()
            return action_target_model._meta.verbose_name

        return self.target_type_verbose_name

    def get_action_display_pattern(self):

        return Actions.get_action_display_pattern(self.action)

    def display_anonimuos(self):

        return self.ANONIMUOS_DISPLAY_TEXT

    def get_reputation_deviation(self):

        return Actions.get_reputation_deviation(self.action, self.target_content_type)
