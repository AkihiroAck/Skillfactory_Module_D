import django_filters

from django import forms
from .models import Post, Category


class ProductFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains')
    category = django_filters.ModelChoiceFilter(queryset=Category.objects.all())
    creation_time = django_filters.DateFilter(field_name='creation_time', lookup_expr='date', widget=forms.DateInput(attrs={'type': 'date'}))
    
    class Meta:
        model = Post
        fields = [
            'title',
            'category',
            'creation_time',
        ]
