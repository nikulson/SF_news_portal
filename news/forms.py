from django.forms import ModelForm, BooleanField
from .models import Post


# Создаём модельную форму
class PostForm(ModelForm):
    check_box = BooleanField(label='Готово')  # добавляем галочку, или же true-false поле
    # в класс мета, как обычно, надо написать модель, по которой будет строится форма и нужные нам поля. Мы уже делали что-то похожее с фильтрами.
    class Meta:
        model = Post
        fields = ['post_type', 'post_title', 'post_text', 'authors', 'post_categories', 'check_box']