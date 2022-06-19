from django import forms
from django.forms import Textarea
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
# from captcha.fields import CaptchaField
from easy_thumbnails.widgets import ImageClearableFileInput
from django.forms.utils import ErrorList

from .models import *


class ProductForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cat'].emptylabel = 'Категория не выбрана'
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    class Meta:
        model = Product
        fields = ['act', 'title', 'slug', 'content', 'price', 'photo', 'is_published', 'cat']
        widgets = {
            'photo': forms.FileInput(attrs={'class': "form-input"}),
            'slug': forms.TextInput(attrs={'class': "form-input"}),
            'price': forms.TextInput(attrs={'class': "form-input", 'type': 'number'}),
            # 'content': forms.Textarea(attrs={'cols': 60, 'rows': 20, 'class': "form-input"})
        }

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) > 200:
            raise ValidationError("Длина превышает 200 символов")
        return title


class ProfileForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    class Meta:
        model = ProfileUser
        fields = ['ava', 'name_author', 'surname_author', 'place_work', 'email', 'master']


class ImageForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    images = forms.ImageField(
        label="Фотографии",
        required=False,
        widget=forms.ClearableFileInput(attrs={"multiple": True}),
    )

    class Meta:
        model = Images
        fields = ("images",)


# class RegisterUserForm(UserCreationForm):
#     username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
#     email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-input'}))
#     password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
#     password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
#
#     class Meta:
#         model = User
#         fields = ('username', 'email', 'password1', 'password2')


# work_rab = ['Осипов', 'Петров', 'Сидоров']


class RegisterUserForm(forms.ModelForm):
    phone_regex = RegexValidator(regex=r'^\+?[78][-\(]?\d{3}\)?-?\d{3}-?\d{2}-?\d{2}$', message="Неверный формат")
    username = forms.CharField(label='Телефон', validators=[phone_regex], max_length=17)  # Validators should be a list
    # password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = User
        fields = ('username', 'password')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
            self.fields['username'].widget.attrs['data-mask'] = "8-000-000-0000"
            self.fields['username'].widget.attrs['placeholder'] = "8-000-000-0000"

    def clean(self):
        super().clean()
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password and password2 and password != password2:
            errors = {'password2': ValidationError('Введённые пароли не совпадают', code='password_mismatch')}
            raise ValidationError(errors)
        else:
            return self.cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password2'])
        if commit:
            user.save()
        return user


class AuthUserForm(AuthenticationForm, forms.ModelForm):
    phone_regex = RegexValidator(regex=r'^\+?[78][-\(]?\d{3}\)?-?\d{3}-?\d{2}-?\d{2}$', message="Неверный формат")
    username = forms.CharField(label='Телефон', validators=[phone_regex], max_length=17)

    class Meta:
        model = User
        fields = ('username', 'password')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
            self.fields['username'].widget.attrs['data-mask'] = "8-000-000-0000"
            self.fields['username'].widget.attrs['placeholder'] = "8-000-000-0000"


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ('text',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
        self.fields['text'].widget = Textarea(attrs={'rows':5})
