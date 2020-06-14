from django import forms


class AddForm(forms.Form):
    description = forms.CharField(max_length=1024)
