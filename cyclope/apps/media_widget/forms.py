from django import forms

class MediaWidgetForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': '2', 'class': 'form-control'}))
    image = forms.ImageField()
    article_id = forms.CharField(widget=forms.HiddenInput)
