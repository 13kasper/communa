from django.db import models
from django.urls import reverse
from .middleware import get_current_user
from django.contrib.auth.models import User
from django.db.models import Q
from PIL import Image


class Product(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Владелец объявления', blank=True, null=True, related_name='my_product')
    readers = models.ManyToManyField(User, related_name='readers', blank=True)
    title = models.CharField(max_length=255, verbose_name='Название')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="Символьный код (на английском)")
    content = models.TextField(blank=True, verbose_name='Описание')
    price = models.CharField(max_length=20, verbose_name='Цена')
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", blank=True, verbose_name='Обложка')
    time_created = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name='Категория')
    act = models.ForeignKey('Act', on_delete=models.PROTECT, verbose_name='Действие')

    def save(self):
        super().save()

        img = Image.open(self.photo.path)

        if img.height > 5000 or img.width > 5000:
            output_size = (5000, 5000)
            img.thumbnail(output_size)
            img.save(self.photo.path)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('ads', kwargs={'ads_slug': self.slug})

    class Meta:
        """Переводим админку на русский"""
        verbose_name = "Объявление"
        verbose_name_plural = "Объявления"
        ordering = ['-time_created']  # сортировка объявлений


class Act(models.Model):
    act_user = models.CharField(max_length=100, db_index=True, verbose_name='Действие')
    act_photo = models.ImageField(upload_to="photos/%Y/%m/%d/", blank=True, verbose_name='Баннер')

    def __str__(self):
        return self.act_user

    class Meta:
        verbose_name = "Действие"
        verbose_name_plural = "Действия"


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name='Категория')
    slug = models.SlugField(max_length=100, unique=True, db_index=True, verbose_name='URL')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Images(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, null=True, blank=True, verbose_name='Альбом')
    images = models.ImageField(upload_to='images/%Y/%m/%d/', verbose_name='Фотоальбом', blank=True)

    def save(self, *args, **kwargs):
        super(Images, self).save(*args, **kwargs)

        img = Image.open(self.images.path)

        if img.height > 5000 or img.width > 5000:
            output_size = (5000, 5000)
            img.thumbnail(output_size)
            img.save(self.images.path)

    class Meta:
        verbose_name = "Фотоальбом"
        verbose_name_plural = "Фотоальбомы"


class StatusFilterComments(models.Manager):
    def get_queryset(self):
        user = get_current_user()
        if not user.is_authenticated:
            return super().get_queryset().filter(status=True)
        return super().get_queryset().filter(
            Q(status=False, author=user) | Q(status=False, product_comment__author=user) | Q(status=True))


class Comments(models.Model):
    product_comment = models.ForeignKey('Product', on_delete=models.CASCADE, null=True, blank=True, verbose_name='key',
                                        related_name='comments_product')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор комментария', blank=True,
                               null=True)
    time_created = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    text = models.TextField(verbose_name="Добавить комментарий")
    status = models.BooleanField(verbose_name="Видимость статьи", default=False)
    objects = StatusFilterComments()

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"


class ProfileUser(models.Model):
    WORK_CHOICES = (
        ('Пресса', 'Пресса'),
        ('Подготовительный участок', 'Подготовительный участок'),
        ('Токарка', 'Токарка'),
        ('ОТК', 'ОТК'),
        ('Радиалки', 'Радиалки'),
        ('Грибки', 'Грибки'),
        ('Роботы', 'Роботы'),
        ('Рубка', 'Рубка'),
        ('Стройка', 'Стройка'),
        ('Механики', 'Механики'),
        ('Электрики', 'Электрики'),
        ('Административный участок', 'Административный участок'),
        ('Дизайнеры', 'Дизайнеры'),
        ('Производство пп и матов', 'Производство пп и матов'),
        ('Производство пасты', 'Производство пасты'),
        ('Типография', 'Типография'),
        ('Склад гот. продукции', 'Склад гот. продукции'),
        ('Склад вулканизации', 'Склад вулканизации'),
        ('Упаковка', 'Упаковка'),
        ('Инструменталка', 'Инструменталка'),
        ('Менеджеры', 'Менеджеры'),
        ('Бухгалтерия', 'Бухгалтерия'),
        ('Обучающий центр', 'Обучающий центр'),
        ('Гараж', 'Гараж'),
        ('Химия', 'Химия'),
        ('Жгуты', 'Жгуты'),
        ('IT-отдел', 'IT-отдел')
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Профиль')
    author_products = models.ForeignKey('Product', on_delete=models.CASCADE, null=True, blank=True, verbose_name='Автор продукта')
    ava = models.ImageField(upload_to="photos/%Y/%m/%d/", blank=True, verbose_name='Аватар')
    name_author = models.CharField(max_length=255, verbose_name='Имя')
    surname_author = models.CharField(max_length=255, verbose_name='Фамилия')
    place_work = models.CharField(max_length=255, choices=WORK_CHOICES, verbose_name='Участок работы')
    phone = models.CharField(max_length=12, verbose_name='Телефон')
    email = models.EmailField(max_length=50, verbose_name='E-mail')
    master = models.BooleanField(verbose_name="Мастер участка", default=False)

    def save(self):
        super().save()

        img = Image.open(self.ava.path)

        if img.height > 3000 or img.width > 3000:
            output_size = (3000, 3000)
            img.thumbnail(output_size)
            img.save(self.ava.path)

    def __str__(self):
        return str(self.user)

    def get_absolute_url(self):
        return reverse('user_profile', kwargs={'pk': self.pk})


class SliderFront(models.Model):
    slide = models.ImageField(upload_to="sliders/%Y/%m/%d/", blank=True, verbose_name='Слайд')
    slide_one = models.ImageField(upload_to="sliders/%Y/%m/%d/", blank=True, verbose_name='Главный_слайд')
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    description = models.CharField(max_length=255, verbose_name='Описание')
    activ = models.BooleanField(default=True, verbose_name='Активность')

    def __str__(self):
        return self.title

    class Meta:
        """Переводим админку на русский"""
        verbose_name = "Слайд фронт"
        verbose_name_plural = "Слайды фронт"









