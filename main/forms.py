from django import forms

class CreateNewPost(forms.Form):
    text = forms.CharField(label="text")
    public = forms.BooleanField(label="Do you want your post to be public?", required=False)
