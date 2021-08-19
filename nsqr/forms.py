from django import forms
from nsqr.models import *


class AddPostForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = ("address",)

    def __init__(self, *args, **kwargs):
        super(AddPostForm, self).__init__(*args, **kwargs)
        self.fields['address'].widget.attrs.update({'class': 'form-control'})