from django.forms import DateInput
from django_filters import FilterSet, CharFilter, DateFilter, ModelChoiceFilter  # импортируем filterset, чем-то напоминающий знакомые дженерики
from .models import Post, Author


# создаём фильтр
class PostFilter(FilterSet):
    title = CharFilter('title',
                       label='Заголовок содержит:',
                       lookup_expr='icontains',
                       )

    body = CharFilter('body',
                            label='Текст содержит:',
                            lookup_expr='icontains',
                            )

    authors = ModelChoiceFilter(field_name='authors',
                                       label='Автор:',
                                       lookup_expr='exact',
                                       queryset=Author.objects.all()
                                       )
    created_at = DateFilter(
        field_name='created_at',
        widget=DateInput(attrs={'type': 'date'}),
        lookup_expr='gt',
        label='Даты позже'
    )

    class Meta:
        model = Post
        fields = []