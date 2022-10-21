from django.db import models

from django.contrib.auth.models import User

from django.db.models import Sum



class Author(models.Model):
    """"Модель, содержащая объекты всех авторов"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    ratingAuthor = models.SmallIntegerField(default=0)

    def update_rating(self):
        postRat = self.post_set.aggregate(postRating=Sum('rating'))
        pRat = 0
        pRat += postRat.get('postRating')

        commentRat = self.user.comment_set.aggregate(commentRating=Sum('rating'))
        cRat = 0
        cRat += commentRat.get('commentRating')

        self.ratingAuthor = pRat *3 + cRat
        self.save()

    def __str__(self):
        return f'{self.user.username}'




class Category(models.Model):
    """"Категории новостей/статей — темы, которые они отражают"""
    category_name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return f'{self.category_name}'


class Post(models.Model):
    """Эта модель должна содержать в себе статьи и новости, которые создают пользователи.
     Каждый объект может иметь одну или несколько категорий."""
    arcticle = 'AR'
    news = 'NW'

    POSITIONS = [
        (arcticle, 'Статья'),
        (news, 'Новость')
    ]
    authors = models.ForeignKey(Author, on_delete=models.CASCADE)
    post_type = models.CharField(max_length=2, choices=POSITIONS, default=arcticle)
    post_pub_date = models.DateTimeField(auto_now_add=True)
    post_categories = models.ManyToManyField(Category, through='PostCategory')
    post_title = models.CharField('Название', max_length=200)
    post_text = models.TextField('Текст')
    rating = models.SmallIntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.post_text[0:123] + '...'

    def __str__(self):
        return f'{self.post_text[0:1200]}'



class PostCategory(models.Model):
    """Промежуточная модель для связи с моделью Post и Category"""
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    """Модель, содержащая комментарии по каждым постом/новостью"""
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.TextField()
    comment_pub_date = models.DateTimeField(auto_now_add=True)
    rating = models.SmallIntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def __str__(self):
        return f'{self.comment_text[0:20]}...'