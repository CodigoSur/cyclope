from django import forms

class MediaWidgetForm(forms.Form):
    image = forms.ImageField()
    name = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    description = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': '2', 'class': 'form-control'}))

class MediaEmbedForm(forms.Form):
    multimedia = forms.FileField()
    name = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    description = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': '2', 'class': 'form-control'}))
    media_type = forms.CharField(required=True, widget=forms.HiddenInput(), initial="picture")
