import random
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from .forms import CustomUserCreationForm,  PasswordResetEmailForm
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from .models import CustomUser
from django.core.mail import send_mail
from django.conf import settings
from .forms import EditProfileForm
from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from groups.models import Group  # Import your Group model
from wishlists.models import Wishlist  # Import the Wishlist model
from friendship.models import FriendRequest
from django.db.models import Q

# Create your views here.
def index(request):
    if request.user.is_authenticated:
        return redirect('accounts:dashboard')  # Use the 'accounts' namespace
    return render(request, 'index.html')

from django.shortcuts import render
from friendship.models import FriendRequest
from wishlists.models import Wishlist
from django.contrib.auth.decorators import login_required
from django.db.models import Q

@login_required
def dashboard(request):
    # Fetch user groups
    user_groups = Group.objects.filter(members=request.user)
    
    # Fetch accepted friends from both directions
    friend_requests = FriendRequest.objects.filter(
        Q(from_user=request.user, status=FriendRequest.ACCEPTED) |
        Q(to_user=request.user, status=FriendRequest.ACCEPTED)
    )
    
    # Create a list of friends (exclude logged-in user)
    friends = []
    for fr in friend_requests:
        if fr.from_user == request.user:
            friends.append(fr.to_user)
        else:
            friends.append(fr.from_user)
    
    # Filter out the logged-in user from the friend list (if included)
    friends = [friend for friend in friends if friend != request.user]
    
    # Fetch wishlists based on visibility settings:
    wishlists = Wishlist.objects.filter(
        Q(user=request.user, visibility='private') |  # Private wishlists visible only to the user
        Q(user__in=friends, visibility='public')  # Public wishlists visible to friends
    )
    
    # Fetch pending friend requests
    pending_requests = FriendRequest.objects.filter(to_user=request.user, status=FriendRequest.PENDING)

    # Prepare context to pass to the template
    context = {
        'user_groups': user_groups,
        'friends': friends,
        'pending_requests': pending_requests,
        'wishlists': wishlists,
    }

    return render(request, 'accounts/dashboard.html', context)








from groups.models import Profile  # Import Profile model

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()  # Save the user
            # Manually create Profile for the newly created user
            Profile.objects.create(user=user)  # Create the Profile instance
            return redirect('accounts:dashboard')  # Redirect to the dashboard or login page after successful registration
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Welcome back to WishCraft!')
            return redirect('index')
        else:
            messages.error(request, 'Invalid username or password. Please try again.')
    
    else:
        form = AuthenticationForm()

    return render(request, 'accounts/login.html', {'form': form})


def custom_logout(request):
    logout(request)
    return redirect('/')

def generate_otp(user):
    otp = str(random.randint(100000,999999))
    return otp 


def forgot_password(request):
    if request.method == "POST":
        form = PasswordResetEmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = CustomUser.objects.get(email=email)
                otp = generate_otp(user)
                request.session['otp'] = otp
                request.session['request_user'] = user.id 
                send_mail(
                    'Password Reset OTP',
                    f'OTP to reset your password is: {otp}',
                    settings.EMAIL_HOST_USER,
                    [user.email],
                    fail_silently=False 
                )
                return redirect('accounts:verify_otp')    
            except CustomUser.DoesNotExist:
                messages.error(request, "No user found with this email")
                return render(request, "accounts/forgot_password.html", {'form': form})
        else:
            return render(request, "accounts/forgot_password.html", {'form': form})
    else:
        form = PasswordResetEmailForm()
    return render(request, "accounts/forgot_password.html", {'form': form})

def verify_otp(request):
    if request.method == 'POST':
        otp_entered = request.POST['otp']
        otp_stored = request.session.get('otp')
        if otp_entered == otp_stored:
            user_id = request.session.get('request_user')
            if user_id:
                user = CustomUser.objects.get(id=user_id)
                return redirect('accounts:reset_password', user_id=user.id)
            else:
                messages.error(request, "Session expired. Please request OTP again.")
                return redirect('accounts:forgot_password')
        else:
            messages.error(request, "Invalid OTP.")
            return render(request, 'accounts/verify_otp.html')
    return render(request, 'accounts/verify_otp.html')

def reset_password(request,user_id):
    user = CustomUser.objects.get(id=user_id)
    if request.method == 'POST':
       form = SetPasswordForm(user = user,data=request.POST)
       if form.is_valid():
           form.save()
           if 'otp' in request.session:
               del request.session['otp']   
           if 'request_user' in request.session:
               del request.session['request_user']
           messages.error(request,"Your Password has been reset succesfully ")
           return redirect('accounts:login')   
    else:
        form = SetPasswordForm(user = user)
    return render(request,'accounts/reset_password.html',{'form':form})


from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model

def view_profile(request, user_id=None):
    # If no user_id is provided, use the logged-in user by default
    user = get_object_or_404(get_user_model(), id=user_id if user_id else request.user.id)
    is_own_profile = request.user.id == user.id  # Check if the logged-in user is viewing their own profile
    return render(request, 'accounts/view_profile.html', {'user': user, 'is_own_profile': is_own_profile})




@login_required
def edit_profile(request):
    if request.method == 'POST':
        # Retrieve user data and update the profile
        user = request.user
        user.username = request.POST.get('username')
        user.email = request.POST.get('email')

        # Update the profile picture if provided
        if request.FILES.get('profile_picture'):
            user.profile_picture = request.FILES['profile_picture']

        user.bio = request.POST.get('bio', user.bio)
        user.date_of_birth = request.POST.get('date_of_birth', user.date_of_birth)
        user.pseudoname = request.POST.get('pseudoname', user.pseudoname)

        user.save()  # Save changes to the user profile

        return redirect('accounts:view_profile', user_id=user.id)  # Redirect to the view profile page

    return render(request, 'accounts/edit_profile.html')

