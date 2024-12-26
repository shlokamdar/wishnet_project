from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
import random
from .models import Group, Profile, generate_group_code
from .forms import GroupForm
from wishlists.models import Wishlist


@login_required
def create_group(request):
    if request.method == "POST":
        form = GroupForm(request.POST)
        if form.is_valid():
            group = form.save(commit=False)
            group.admin = request.user
            group.save()
            group.members.add(request.user)
            
            # Manually create Profile for the user if it doesn't exist
            if not hasattr(request.user, 'profile'):
                Profile.objects.create(user=request.user)
            
            group.assign_secret_santa()
            messages.success(request, f"Group '{group.name}' created successfully!")
            return redirect('groups:group_detail', group_id=group.id)
    else:
        form = GroupForm()
        group_instance = form.save(commit=False)
        group_instance.join_code = generate_group_code()
        form = GroupForm(instance=group_instance)
    
    return render(request, 'groups/create_group.html', {'form': form})


@login_required
def join_group(request):
    if request.method == "POST":
        group_code = request.POST.get('group_code')
        pseudonym = request.POST.get('pseudonym', None)

        try:
            group = Group.objects.get(join_code=group_code)
            if request.user in group.members.all():
                messages.warning(request, "You are already a member of this group.")
            elif group.members.count() < group.group_members_limit:
                group.members.add(request.user)
                if pseudonym:
                    profile, created = Profile.objects.get_or_create(user=request.user)
                    profile.pseudonym = pseudonym
                    profile.save()
                messages.success(request, f"You joined the group '{group.name}' successfully!")
                return redirect('groups:group_detail', group_id=group.id)
            else:
                messages.error(request, "Group is full.")
        except Group.DoesNotExist:
            messages.error(request, "Invalid group code.")
    
    return render(request, 'groups/join_group.html')

from django.db.models import Sum

from django.db.models import Sum, Q
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Sum

@login_required
def group_detail(request, group_id):
    # Fetch the group object by ID
    group = get_object_or_404(Group, id=group_id)
    user = request.user

    # Initialize the assigned member and their wishlists
    assigned_member = None
    assigned_member_wishlists = None

    # Check if Secret Santa has been assigned for the group
    if group.secret_santa_assigned:
        # Get the assigned member for the current user (Secret Santa recipient)
        # The profile must have a field indicating the assigned person
        assigned_member = group.members.filter(profile__secret_santa_assigned_to=user).first()

        if assigned_member:
            # If an assigned member exists, fetch their wishlists for the group within the budget
            assigned_member_wishlists = assigned_member.wishlists.filter(
                groups=group  # Only wishlists associated with the current group
            ).annotate(
                total_price=Sum('items__price_range')  # Sum up the price range of wishlist items
            ).filter(
                total_price__lte=group.budget_limit  # Ensure wishlist total is within the budget limit
            ).distinct()

    # Retrieve all the wishlists in the group, ensuring that they fit within the budget
    wishlists = group.wishlists.annotate(
        total_price=Sum('items__price_range')
    ).filter(
        total_price__lte=group.budget_limit  # Ensure total price is within the budget limit
    ).distinct()

    # Pass all relevant data to the template
    return render(request, 'groups/group_detail.html', {
        'group': group,
        'wishlists': wishlists,
        'assigned_member': assigned_member,
        'assigned_member_wishlists': assigned_member_wishlists,
    })



@login_required
def user_groups(request):
    groups = Group.objects.filter(members=request.user)
    return render(request, 'groups/user_groups.html', {'groups': groups})

@login_required
def leave_group(request, group_id):
    group = get_object_or_404(Group, id=group_id)

    if group.admin == request.user:
        if group.members.count() == 1:
            messages.error(request, "You cannot leave the group as the only member. Please delete or transfer the group first.")
        else:
            messages.error(request, "Admins cannot leave their own groups. Assign another admin first.")
    else:
        group.members.remove(request.user)
        messages.success(request, f"You left the group '{group.name}' successfully!")
        return redirect('groups:user_groups')
    
    return redirect('groups:group_detail', group_id=group_id)

@login_required
def remove_member(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    if request.method == "POST" and request.user == group.admin:
        member_id = request.POST.get('member_id')
        member = get_object_or_404(get_user_model(), id=member_id)
        group.members.remove(member)
    return redirect('groups:group_detail', group_id=group.id)

from django.shortcuts import render, get_object_or_404, redirect
from groups.models import Group
from django.contrib import messages

# Function to map price range to a numeric value
def get_price_range_value(price_range):
    price_mapping = {
        '0_100': 50,    # Example: consider mid-range of the range
        '101_200': 150,
        '201_300': 250,
        '301_500': 400,
        '501_1000': 750,
        '1001_2000': 1500,
        '2001_5000': 3500,
        '5001_above': 6000
    }
    return price_mapping.get(price_range, 0)  # Default to 0 if no match

@login_required
def add_wishlist_to_group(request, group_id):
    group = get_object_or_404(Group, id=group_id)

    if request.user in group.members.all():
        if request.method == "POST":
            wishlist_id = request.POST.get('wishlist')
            wishlist = get_object_or_404(Wishlist, id=wishlist_id)

            # Calculate the total price by summing the values of price_range
            total_price = sum(get_price_range_value(item.price_range) for item in wishlist.items.all())

            # Check if the total price exceeds the group’s budget limit
            if total_price > group.budget_limit:
                messages.error(request, f"Your wishlist exceeds the group's budget limit of {group.budget_limit}!")
            else:
                group.wishlists.add(wishlist)
                group.save()
                messages.success(request, f"Wishlist '{wishlist.title}' added to the group successfully!")

            return redirect('groups:group_detail', group_id=group.id)

    return redirect('groups:group_detail', group_id=group.id)



@login_required
def assign_secret_santa(request, group_id):
    group = get_object_or_404(Group, id=group_id)

    if request.user == group.admin:
        members = list(group.members.all())
        if len(members) < 2:
            return redirect('groups:group_detail', group_id=group.id)

        for member in members:
            if not hasattr(member, 'profile'):
                Profile.objects.create(user=member)

        random.shuffle(members)
        profiles_to_update = []
        for i, member in enumerate(members):
            assigned_member = members[(i + 1) % len(members)]
            profile = member.profile
            profile.secret_santa_assigned_to = assigned_member
            profiles_to_update.append(profile)

        with transaction.atomic():
            Profile.objects.bulk_update(profiles_to_update, ['secret_santa_assigned_to'])

        group.secret_santa_assigned = True
        group.save()
        messages.success(request, f"Secret Santa has been successfully assigned for group {group.name}.")

    return redirect('groups:group_detail', group_id=group.id)
