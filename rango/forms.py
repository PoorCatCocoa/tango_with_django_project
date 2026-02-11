from django import forms
from rango.models import Page, Category

class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=128,
                           help_text="Please enter the category name.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        # Associate this form with the Category model.
        model = Category
        fields = ('name',)

class PageForm(forms.ModelForm):
    title = forms.CharField(max_length=128,
                            help_text="Please enter the title of the page.")
    url = forms.URLField(max_length=200,
                         help_text="Please enter the URL of the page.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    class Meta:
        model = Page
        exclude = ('category',)

    # This is a data cleaning method that ensures URLs begin with the prefix http://.
    def clean(self):
        cleaned_data = self.cleaned_data
        url = cleaned_data.get('url')

        # If the URL is not empty and does not start with http:// or https://, add automatically.
        if url and not url.startswith('http://') and not url.startswith('https://'):
            url = f'http://{url}'
            cleaned_data['url'] = url

        return cleaned_data