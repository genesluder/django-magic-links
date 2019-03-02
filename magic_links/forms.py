from django import forms


class MagicLinkForm(forms.Form):    
    email = forms.EmailField()
    next = forms.CharField(required=False, widget=forms.HiddenInput())
