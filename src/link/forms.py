from django import forms

from link.models import ProtectedResource


class ProtectedResourceForm(forms.ModelForm):
    uri = forms.URLField(required=False)
    file = forms.FileField(required=False)

    class Meta:
        model = ProtectedResource
        fields = ['uri', 'file']

    def clean(self):
        cleaned_data = super(ProtectedResourceForm, self).clean()

        uri = cleaned_data.get('uri')
        file = cleaned_data.get('file')

        if (uri and file) or (not uri and not file):
            self.add_error('uri', "Please select only URI or FILE to protect")

        return cleaned_data


class PasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput())
