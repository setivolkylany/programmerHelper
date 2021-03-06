
from django.contrib.sessions.backends.db import SessionStore as CachedDBStore


class SessionStore(CachedDBStore):

    cache_key_prefix = 'sessions.extended_cached_db_backend'

    @classmethod
    def get_model_class(cls):
        from apps.sessions.models import ExpandedSession
        return ExpandedSession

    def create_model_instance(self, data):
        obj = super(SessionStore, self).create_model_instance(data)
        try:
            account_pk = data.get('_auth_user_id')
        except (ValueError, TypeError):
            account_pk = None
        obj.account_pk = account_pk
        return obj
