import django_filters.rest_framework as filters

from src.Announcements.models import (
    Announcement,
    category_choices
)

ANNOUNCEMENT_CATEGORY_CHOICES = (
    ('Демедж Диллер', "ДД"),
    ("ДД", "Демедж Диллер"),
)


class AnnouncementListFilter(filters.FilterSet):
    title__icontains = filters.CharFilter(field_name='title', lookup_expr='icontains')
    description__icontains = filters.CharFilter(field_name="description", lookup_expr='icontains')
    create_date__lte = filters.DateTimeFilter(field_name='create_date', lookup_expr='lte')
    create_date__gte = filters.DateTimeFilter(field_name='create_date', lookup_expr='gte')

    category = filters.ChoiceFilter(choices=category_choices)

    o = filters.filters.OrderingFilter(
        choices=(
            ('create_date', 'create_date'),
        ),
        fields={
            'create_date': '-create_date',
        }
    )

    class Meta:
        model = Announcement
        fields = ['description']
