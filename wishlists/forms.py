# forms.py
from django import forms
from .models import Wishlist, WishlistItem

class WishlistForm(forms.ModelForm):
    class Meta:
        model = Wishlist
        fields = ['title', 'description', 'visibility', 'group', 'category']
        category = forms.ChoiceField(choices=Wishlist.CATEGORY_CHOICES, initial='other')

    def clean(self):
        cleaned_data = super().clean()
        group = cleaned_data.get('group')  # Get the group associated with the wishlist

        # Ensure that the group is valid
        if group:
            total_price = 0
            # Calculate total price based on the wishlist items (which are added separately)
            items = WishlistItem.objects.filter(wishlist__group=group)  # Assuming wishlist items are linked to a group

            for item in items:
                total_price += item.price_range  # Assuming price_range is an integer value

            if total_price > group.budget_limit:
                raise forms.ValidationError("Total price of items exceeds the group's budget limit.")

        return cleaned_data
# forms.py
class WishlistItemForm(forms.ModelForm):
    class Meta:
        model = WishlistItem
        fields = ['name', 'description', 'price_range', 'url', 'image']
        price_range = forms.ChoiceField(choices=WishlistItem.RANGE_CHOICES, initial='0_100')  # Default to '0 to 100'


# forms.py

from django import forms
from wishlists.models import Wishlist

class AddWishlistToGroupForm(forms.Form):
    wishlist = forms.ModelChoiceField(queryset=Wishlist.objects.all(), label="Select Wishlist")
