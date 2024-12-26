from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from friendship.forms import UserSearchForm
from .models import FriendRequest
from django.contrib.auth import get_user_model

@login_required
def send_friend_request(request, user_id):
    to_user = get_object_or_404(get_user_model(), id=user_id)

    # Check if the user is trying to send a request to themselves
    if request.user == to_user:
        messages.error(request, "You cannot send a friend request to yourself.")
        return redirect('accounts:view_profile', user_id=user_id)

    # Check if a pending request already exists
    if FriendRequest.objects.filter(from_user=request.user, to_user=to_user, status='Pending').exists():
        messages.error(request, "You have already sent a friend request.")
        return redirect('accounts:view_profile', user_id=user_id)

    # Create a new friend request
    FriendRequest.objects.create(from_user=request.user, to_user=to_user, status='Pending')
    messages.success(request, f"Friend request sent to {to_user.username}.")

    # Redirect to the dashboard
    return redirect('accounts:dashboard')


@login_required
def remove_friend(request, user_id):
    to_user = get_object_or_404(get_user_model(), id=user_id)

    # Check if they are friends (look for accepted friend requests in either direction)
    friendship = FriendRequest.objects.filter(
        from_user=request.user,
        to_user=to_user,
        status='Accepted'
    ) | FriendRequest.objects.filter(
        from_user=to_user,
        to_user=request.user,
        status='Accepted'
    )

    # If there's no friendship, show an error message
    if not friendship.exists():
        messages.error(request, "You are not friends with this user.")
        return redirect('accounts:view_profile', user_id=user_id)

    # If there's a friendship, delete it
    friendship.delete()
    messages.success(request, f"You have removed {to_user.username} as a friend.")
    
    # Redirect to the dashboard after removing the friend
    return redirect('accounts:dashboard')


# View all friend requests
@login_required
def view_friend_requests(request):
    sent_requests = FriendRequest.objects.filter(from_user=request.user)
    received_requests = FriendRequest.objects.filter(to_user=request.user, status='Pending')
    
    # Debugging: Print the received requests to see if they are retrieved correctly
    print("Received Requests:")
    for req in received_requests:
        print(f"Request ID: {req.id}, From: {req.from_user.username}, Status: {req.status}")
    
    context = {
        'sent_requests': sent_requests,
        'received_requests': received_requests,
    }
    return render(request, 'friendship/view_request.html', context)



# Accept a friend request
def accept_friend_request(request, request_id):
    # Get the friend request
    friend_request = get_object_or_404(FriendRequest, id=request_id)

    # Check if the logged-in user is the recipient of the friend request
    if friend_request.to_user != request.user:
        messages.error(request, "You can only accept friend requests addressed to you.")
        return redirect('accounts:dashboard')

    # If the friend request is not already accepted, update the status to 'Accepted'
    if friend_request.status != 'Accepted':
        friend_request.status = 'Accepted'
        friend_request.save()
        messages.success(request, f"You have accepted {friend_request.from_user.username}'s friend request.")
    else:
        messages.info(request, "This friend request has already been accepted.")

    return redirect('accounts:dashboard')

# Reject a friend request
@login_required
def reject_friend_request(request, request_id):
    friend_request = get_object_or_404(FriendRequest, id=request_id, to_user=request.user, status='Pending')
    
    friend_request.status = 'Rejected'
    friend_request.save()
    
    messages.success(request, f"You rejected the friend request from {friend_request.from_user.username}.")
    return redirect('friendship:view_requests')


def search_user(request):
    form = UserSearchForm(request.GET)
    users = []
    if form.is_valid():
        username = form.cleaned_data['username']
        users = get_user_model().objects.filter(username__icontains=username)  # Case-insensitive search
    return render(request, 'friendship/search_user.html', {'form': form, 'users': users})