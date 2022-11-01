from django.db import models

from django.contrib.auth.models import User

from django.db.models import Sum


class Author(models.Model):
    """"Модель, содержащая объекты всех авторов"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.SmallIntegerField(default=0)

    def update_rating(self):
        post_rat = self.post_set.aggregate(post_rating=Sum('rating'))
        p_rat = 0
        p_rat += post_rat.get('post_rating')

        comment_rat = self.user.comment_set.aggregate(comment_rating=Sum('rating'))
        c_rat = 0
        c_rat += comment_rat.get('comment_rating')

        self.rating = p_rat *3 + c_rat
        self.save()

    def __str__(self):
        return f'{self.user.username}'


class Category(models.Model):
    """"Категории новостей/статей — темы, которые они отражают"""
    name = models.CharField(max_length=200, unique=True, null=False)
    subscribers = models.ManyToManyField(User, max_length=200, blank=True)

    def __str__(self):
        return f'{self.name}'


class Post(models.Model):
    """Эта модель должна содержать в себе статьи и новости, которые создают пользователи.
     Каждый объект может иметь одну или несколько категорий."""
    article = 'AR'
    news = 'NW'

    POSITIONS = [
        (article, 'Статья'),
        (news, 'Новость')
    ]
    type = models.CharField(max_length=2, choices=POSITIONS, default=article)
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField('Название', max_length=200)
    body = models.TextField('Текст')
    rating = models.SmallIntegerField(default=0)
    authors = models.ForeignKey(Author, on_delete=models.CASCADE, null=False)
    category = models.ManyToManyField(Category, through='PostCategory')

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.body[0:123] + '...'

    def get_absolute_url(self):
        return f'/news/{self.id}'

    def __str__(self):
        return f'{self.body[0:1200]}'


class PostCategory(models.Model):
    postThrough = models.ForeignKey(Post, on_delete=models.CASCADE)
    categoryThrough = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    """Модель, содержащая комментарии по каждым постом/новостью"""
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.SmallIntegerField(default=0)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    
    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def __str__(self):
        return f'{self.text[0:20]}...'