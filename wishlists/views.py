from django.shortcuts import render, redirect, get_object_or_404
from .forms import WishlistForm, WishlistItemForm
from .models import Wishlist, WishlistItem
from groups.models import Group
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.contrib import messages

def create_wishlist(request):
    if request.method == 'POST':
        wishlist_form = WishlistForm(request.POST)
        item_form = WishlistItemForm(request.POST, request.FILES)

        if wishlist_form.is_valid() and item_form.is_valid():
            wishlist = wishlist_form.save(commit=False)
            wishlist.user = request.user
            wishlist.save()

            item = item_form.save(commit=False)
            item.wishlist = wishlist
            item.save()

            return redirect('wishlists:wishlist_list', user_id=request.user.id)
        else:
            print("Form errors:", wishlist_form.errors, item_form.errors)

    else:
        wishlist_form = WishlistForm()
        item_form = WishlistItemForm()

    user_groups = Group.objects.filter(members=request.user)

    return render(request, 'wishlists/create.html', {
        'wishlist_form': wishlist_form,
        'item_form': item_form,
        'groups': user_groups
    })

def wishlist_list(request, user_id=None):
    user = get_object_or_404(get_user_model(), id=user_id if user_id else request.user.id)
    wishlists = Wishlist.objects.filter(user=user)

    if request.user != user:
        wishlists = wishlists.filter(visibility='public')

    is_own_wishlists = (request.user.id == user.id)

    return render(request, 'wishlists/wishlist_list.html', {
        'wishlists': wishlists,
        'user': user,
        'is_own_wishlists': is_own_wishlists,
    })

def wishlist_detail(request, pk):
    wishlist = get_object_or_404(Wishlist, pk=pk)
    share_url = request.build_absolute_uri(reverse('wishlists:share_wishlist', args=[wishlist.id]))
    items = wishlist.items.all()
    
    # Pass the logged-in user to the template
    return render(request, 'wishlists/wishlist_detail.html', {
        'wishlist': wishlist, 
        'items': items, 
        'share_url': share_url,
        'user': request.user  # Pass the logged-in user to the template
    })

def edit_wishlist(request, pk):
    wishlist = get_object_or_404(Wishlist, pk=pk)
    wishlist_item = wishlist.items.first() if wishlist.items.exists() else None

    if request.method == 'POST':
        wishlist_form = WishlistForm(request.POST, instance=wishlist)
        item_form = WishlistItemForm(request.POST, request.FILES, instance=wishlist_item)

        if wishlist_form.is_valid() and item_form.is_valid():
            wishlist_form.save()

            item = item_form.save(commit=False)
            item.wishlist = wishlist
            item.save()

            messages.success(request, "Wishlist and item updated successfully!")
            return redirect('wishlists:wishlist_detail', pk=wishlist.pk)
    else:
        wishlist_form = WishlistForm(instance=wishlist)
        item_form = WishlistItemForm(instance=wishlist_item)

    return render(request, 'wishlists/edit_wishlist.html', {
        'wishlist_form': wishlist_form,
        'item_form': item_form,
        'wishlist': wishlist,
        'existing_item': wishlist_item,
    })

def add_item(request, wishlist_id):
    wishlist = get_object_or_404(Wishlist, id=wishlist_id)
    if request.method == "POST":
        form = WishlistItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.wishlist = wishlist
            item.save()
            return redirect('wishlists:wishlist_detail', pk=wishlist.id)
    else:
        form = WishlistItemForm()
    return render(request, 'wishlists/add_item.html', {'form': form, 'wishlist': wishlist})

def edit_item(request, pk):
    item = get_object_or_404(WishlistItem, pk=pk)
    if request.method == "POST":
        form = WishlistItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            return redirect('wishlists:wishlist_detail', pk=item.wishlist.id)
    else:
        form = WishlistItemForm(instance=item)
    return render(request, 'wishlists/edit_item.html', {'form': form, 'item': item})

def delete_item(request, pk):
    item = get_object_or_404(WishlistItem, pk=pk)
    wishlist_id = item.wishlist.id
    if request.method == "POST":
        item.delete()
        return redirect('wishlists:wishlist_detail', pk=wishlist_id)
    return render(request, 'wishlists/delete_item.html', {'item': item})

def share_wishlist(request, wishlist_id):
    wishlist = get_object_or_404(Wishlist, id=wishlist_id)
    return render(request, 'wishlists/share_wishlist.html', {'wishlist': wishlist})
