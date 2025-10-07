from typing import Any
from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError

from accounts.models import User


class UserCreationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password = forms.CharField(
        label='Password confirmation',
        widget=forms.PasswordInput
        )

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'phone')

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 != password2 and password2 and password1:
            raise ValidationError('Passwords don\'t much')

        return password2

    def save(self, commit=True) -> Any:
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = (
            'email',
            'first_name',
            'last_name',
            'phone'
        )


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('email', 'registrated_at', 'is_admin')
    list_filter = ('registrated_at', 'is_admin',)
    fieldsets = [
        (None, {'fields': ['email', 'password']}),
        ('Personal info', {'fields': ['first_name', 'last_name', 'phone']}),
        ('Permissions', {'fields': ['is_admin']}),
    ]
    add_fieldsets = [
        (
            None,
            {
                'classes': ['wide'],
                'fields': [
                    'email',
                    'first_name',
                    'last_name',
                    'phone',
                    'password1',
                    'password2'
                    ],
            },
        ),
    ]
    search_fields = ('email',)
    ordering = ('-registrated_at', 'email')
    filter_horizontal = []


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
