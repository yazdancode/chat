from django import forms
from django.forms import ModelForm

from User.models import Profile


class UserForm(ModelForm):
    class Meta:
        model = Profile
        exclude = ["user"]
        labels = {
            "image": "عکس",
            "username": "نام کاربری",
            "email": "ایمیل",
            "password": "رمز عبور",
            "location": "مکان",
            "bio": "توضیحات",
        }
        widgets = {
            "image": forms.FileInput(
                attrs={
                    "class": "form-control",
                    "accept": "image/*",
                    "style": "background-color: #e3f2fd; font-size: 14px; border: 1px solid #90caf9; padding: 8px; border-radius: 4px;",
                    "placeholder": "لینک عکس را وارد کنید",
                    "type": "file",
                    "id": "id_image",
                }
            ),
            "username": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "نام کاربری خود را وارد کنید",
                    "style": "font-size: 14px; border: 1px solid #90caf9; padding: 8px; border-radius: 4px;",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "ایمیل خود را وارد کنید",
                    "style": "font-size: 14px; border: 1px solid #90caf9; padding: 8px; border-radius: 4px;",
                }
            ),
            "password": forms.PasswordInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "رمز عبور خود را وارد کنید",
                    "style": "font-size: 14px; border: 1px solid #90caf9; padding: 8px; border-radius: 4px;",
                }
            ),
            "location": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "مکان خود را وارد کنید",
                    "style": "font-size: 14px; border: 1px solid #90caf9; padding: 8px; border-radius: 4px;",
                }
            ),
            "bio": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "توضیحات خود را وارد کنید",
                    "rows": 3,
                    "style": "font-size: 14px; border: 1px solid #90caf9; padding: 8px; border-radius: 4px;",
                }
            ),
        }
