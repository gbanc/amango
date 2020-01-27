from django import forms

from profiles.models import Profile


class AddProfileForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(AddProfileForm, self).__init__(*args, **kwargs)

        if self.request.user.is_superuser:
            return

        self.fields['user'] = forms.ChoiceField(self.request.user)

    class Meta:
        model = Profile
        exclude = ('user',)

