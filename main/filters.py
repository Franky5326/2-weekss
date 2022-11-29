import django_filters
from .models import Applications


class CategoryFilters(django_filters.FilterSet):
    class Meta:
        model = Applications
        exclude = ['img']
        fields = ['category']
