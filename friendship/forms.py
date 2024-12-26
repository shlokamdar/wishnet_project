from django import forms

class UserSearchForm(forms.Form):
    username = forms.CharField(max_length=100, label='Search for a user', required=True)