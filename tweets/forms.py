from django import forms

from .models import Tweet

MAX_TWEET_LENGTH = 240


class TweetForm(forms.ModelForm):
    # content = forms.Charfield()   # to change
    class Meta:                           # describes the form
        model = Tweet
        fields =['content']

    def clean_content(self):    # custom validation
        content = self.cleaned_data.get('content')    # to get the content
        if len(content) > MAX_TWEET_LENGTH:
            raise forms.ValidationError("This tweet is too long")
        return content
