from django.db import models
from users.models import CustomUser


class News(models.Model):
    date = models.DateField(verbose_name="Дата")
    title = models.CharField(max_length=255, verbose_name="Название")
    text = models.TextField(verbose_name="Текст")
    author = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE,
        verbose_name="Автор")
    likes_count = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
    
    def __str__(self):
        return self.title


class Comment(models.Model):
    date = models.DateField(verbose_name="Дата")
    text = models.TextField(verbose_name="Текст")
    author = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE,
        verbose_name="Автор")
    news = models.ForeignKey(
        News, on_delete=models.CASCADE,
        verbose_name="Новости")

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'


class Like(models.Model):
    user = models.ForeignKey(
        CustomUser,on_delete=models.CASCADE,
        related_name='likes',
        verbose_name="Пользователь")
    news = models.ForeignKey(
        News, on_delete=models.CASCADE,
        related_name='likes',
        verbose_name="Новости")

    class Meta:
        verbose_name = 'Лайк'
        verbose_name_plural = 'Лайки'