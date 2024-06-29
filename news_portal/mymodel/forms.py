from django import forms
from .models import Post, Category, Author, TYPE
from django.core.exceptions import ValidationError


class PostForm(forms.ModelForm):
    title = forms.CharField(
        min_length=4,
        max_length=50,
        widget=forms.TextInput(attrs={'style': 'width: 300px;'}),  # Пример задания ширины в пикселях
    )
    
    type = forms.ChoiceField(
        choices=TYPE,
        required=True,
    )
    
    category = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-control', 'style': 'margin-top: 10px;'}),
    )
    
    text = forms.CharField(
        min_length=10,
        max_length=2500,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 10, 'style': 'margin-top: 10px; width: 100%;'}),  # Пример задания ширины и высоты в пикселях
    )

    authors = forms.ModelChoiceField(
        queryset=Author.objects.all(),
        widget=forms.Select(attrs={'class': ''}),
        required=True
    )
    
    class Meta:
        model = Post
        fields = [
            'title',
            'type',
            'category',
            'text',
            'authors',
        ]
        