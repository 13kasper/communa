from django.contrib import admin
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.utils.safestring import mark_safe

from django import forms

from .models import *


class ProductAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Product
        fields = '__all__'


class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm
    prepopulated_fields = {'slug': ('title',)}
    """устанавливаем в админке отображение полей"""
    list_display = ('id', 'title', 'time_created', 'get_html_photo', 'is_published')
    """Список отображаемых ссылок"""
    list_display_links = ('id', 'title')
    """Добавление поиска"""
    search_fields = ('title', 'content')
    """Редактируем чекбоксы (вкл/выкл)"""
    list_editable = ('is_published',)
    """Фильтрация в админке"""
    list_filter = ('is_published', 'time_created')
    """Какие поля хотим видеть """
    fields = ('author', 'title', 'slug', 'cat', 'content', 'photo', 'get_html_photo', 'is_published', 'time_created', 'time_update')
    """Поля для чтения"""
    readonly_fields = ('get_html_photo', 'time_created', 'time_update')
    """Добавляем панель управления наверх"""
    save_on_top = True

    """Для отображения фотографий в админке"""
    def get_html_photo(self, object):
        if object.photo:
            return mark_safe(f"<img src='{object.photo.url}' width='50'>")

    """меняем в админке название методу"""
    get_html_photo.short_description = 'Миниатюра'


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)


# class ImagesAdmin(admin.ModelAdmin):
#     prepopulated_fields = {'slug': ('images',)}


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Images)
admin.site.register(Comments)
admin.site.register(ProfileUser)
admin.site.register(Act)
admin.site.register(SliderFront)
# admin.site.register(UserFavorites)
