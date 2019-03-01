from django import forms


class MagicLinkForm(forms.Form):    
    email = forms.EmailField()
