from django.forms import DateInput
from django_filters import FilterSet, CharFilter, DateFilter, ModelChoiceFilter  # импортируем filterset, чем-то напоминающий знакомые дженерики
from .models import Post, Author


# создаём фильтр
class PostFilter(FilterSet):
    post_title = CharFilter('post_title',
                       label='Заголовок содержит:',
                       lookup_expr='icontains',
                       )

    post_text = CharFilter('post_text',
                            label='Текст содержит:',
                            lookup_expr='icontains',
                            )

    authors = ModelChoiceFilter(field_name='authors',
                                       label='Автор:',
                                       lookup_expr='exact',
                                       queryset=Author.objects.all()
                                       )
    post_pub_date = DateFilter(
        field_name='post_pub_date',
        widget=DateInput(attrs={'type': 'date'}),
        lookup_expr='gt',
        label='Даты позже'
    )

    class Meta:
        model = Post
        fields = []