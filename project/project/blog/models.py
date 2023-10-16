from django.db import models
from django.urls import reverse


class Category(models.Model):
    title = models.CharField(max_length=200,
                             unique=True,
                             verbose_name='Название категории')

    def get_absolute_url(self):
        return reverse('category', kwargs={'category_id': self.pk})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Article(models.Model):
    title = models.CharField(max_length=200,
                             unique=True,
                             verbose_name='Название статьи')
    content = models.TextField(verbose_name='Содержание статьи')
    photo = models.ImageField(upload_to='photos/', blank=True, null=True, verbose_name='Фотография')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновление')
    publish = models.BooleanField(default=0, verbose_name='Статус публикации')
    views = models.IntegerField(default=0, verbose_name='Количество просмотров')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория статьи')

    def get_photo(self):
        if self.photo:
            return self.photo.url
        else:
            return 'https://shv48.ru/assets/cache_image/no-photo_250x250_3af.jpg'

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'


class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title
