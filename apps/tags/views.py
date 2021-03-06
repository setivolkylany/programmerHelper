
from django.views.generic import DetailView

from .models import Tag


class TagDetailView(DetailView):
    model = Tag
    template_name = "tags/detail.html"
    slug_url_kwarg = 'name'
    slug_field = 'name'
