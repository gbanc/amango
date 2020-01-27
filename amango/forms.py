
from django.contrib.auth.forms import AuthenticationForm
from django import forms

class UserAdminAuthenticationForm(AuthenticationForm):
    """
    Same as Django's AdminAuthenticationForm but allows to login
    any user who is not staff.
    """
    this_is_the_login_form = forms.BooleanField(widget=forms.HiddenInput,
                                initial=1,
                                error_messages={'required':
                                "Please log in again, because your session has"
                                " expired."})
