
from django.conf.urls import url

from .views import TagDetailView

app_name = 'tags'

urlpatterns = [
    url(r'tag/(?P<name>[-_\w]+)/$', TagDetailView.as_view(), {}, 'tag'),
]
