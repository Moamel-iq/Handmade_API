from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm, ReadOnlyPasswordHashField
from django import forms
from django.urls import reverse_lazy

from account.models import EmailAccount


class UserAdminChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].help_text = (
                                                "Raw passwords are not stored, so there is no way to see "
                                                "this user's password, but you can <a href=\"%s\"> "
                                                "<strong>Change the Password</strong> using this form</a>."
                                            ) % reverse_lazy('admin:auth_user_password_change', args=[self.instance.id])

    class Meta:
        model = EmailAccount
        fields = ('email', 'password')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]