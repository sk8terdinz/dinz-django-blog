from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Profile, MyUpdate
from .forms import UpdateForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django import forms

# Create your views here.

def home(request):
    if request.user.is_authenticated:
        form = UpdateForm(request.POST or None)
        if request.method == "POST":
            if form.is_valid():
                weep = form.save(commit=False)
                weep.user = request.user
                weep.save()
                messages.success(request, ("Your Update Has Been Posted!"))
                return redirect('home')

        weeps = MyUpdate.objects.all().order_by("-created_at")
        return render(request, 'home.html', {"weeps":weeps, "form":form})
    else:
        weeps = MyUpdate.objects.all().order_by("-created_at")
        return render(request, 'home.html', {"weeps":weeps})


def profile_list(request):
    if request.user.is_authenticated:
        profiles = Profile.objects.exclude(user=request.user)
        return render(request, 'profile_list.html', {"profiles":profiles})
    else:
        messages.success(request, ("You Must Be Logged In To View This Page..."))
        return redirect('home')
    
def profile(request, pk):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user_id=pk)
        weeps = MyUpdate.objects.filter(user_id=pk).order_by("-created_at")
        # Post Form Logic
        if request.method == "POST":
            # Get current user
            current_user_profile = request.user.profile
            # Get form data
            action = request.POST['follow']
            # Decide to follow or unfollow
            if action == "unfollow":
                current_user_profile.follows.remove(profile)
            elif action == "follow":
                current_user_profile.follows.add(profile)
            # Save the profile
            current_user_profile.save()
                
        return render(request, "profile.html", {"profile":profile, "weeps":weeps})
    else:
        messages.success(request, ("You Must Be Logged In To View This Page..."))
        return redirect('home')
    
def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, ("You Have Been Logged In!"))
            return redirect('home')
        else:
            messages.success(request, ("There was an error logging in. Try again!"))
            return redirect('login')
    else:
        return render(request, "login.html", {})

def logout_user(request):
    logout(request)
    messages.success(request, ("There Have Been Logged Out. See You again!"))
    return redirect('home')

def register_user(request):
    return render(request, "register.html", {})