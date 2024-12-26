from django import forms
from .models import Group

class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'budget_limit', 'group_members_limit', 'join_code']
        widgets = {
            'join_code': forms.TextInput(attrs={'readonly': 'readonly'})  # Make join_code readonly
        }


